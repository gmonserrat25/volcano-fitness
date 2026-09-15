// Arma un mp4 a partir de JPEGs numerados, con el ritmo exacto que se le pida.
// Uso: armar <carpeta> <salida.mp4> <fps>
import Foundation
import AVFoundation
import AppKit

let args = CommandLine.arguments
guard args.count >= 4 else { print("uso: armar <carpeta> <salida> <fps>"); exit(1) }
let carpeta = args[1], salida = args[2], fps = Int32(args[3]) ?? 25

let fm = FileManager.default
let archivos = (try! fm.contentsOfDirectory(atPath: carpeta))
    .filter { $0.hasSuffix(".jpg") }.sorted()
guard !archivos.isEmpty else { print("sin jpgs"); exit(1) }

let primera = NSImage(contentsOfFile: "\(carpeta)/\(archivos[0]))".replacingOccurrences(of: ")", with: ""))!
var rect = NSRect(origin: .zero, size: primera.size)
let cg0 = primera.cgImage(forProposedRect: &rect, context: nil, hints: nil)!
let W = cg0.width, H = cg0.height

try? fm.removeItem(atPath: salida)
let writer = try! AVAssetWriter(outputURL: URL(fileURLWithPath: salida), fileType: .mp4)
let ajustes: [String: Any] = [
    AVVideoCodecKey: AVVideoCodecType.h264,
    AVVideoWidthKey: W, AVVideoHeightKey: H,
    AVVideoCompressionPropertiesKey: [
        AVVideoAverageBitRateKey: Int(ProcessInfo.processInfo.environment["BR"] ?? "1600000")!,
        AVVideoProfileLevelKey: AVVideoProfileLevelH264HighAutoLevel,
        AVVideoMaxKeyFrameIntervalKey: fps * 2
    ]
]
let entrada = AVAssetWriterInput(mediaType: .video, outputSettings: ajustes)
entrada.expectsMediaDataInRealTime = false
let adaptador = AVAssetWriterInputPixelBufferAdaptor(
    assetWriterInput: entrada,
    sourcePixelBufferAttributes: [
        kCVPixelBufferPixelFormatTypeKey as String: Int(kCVPixelFormatType_32ARGB),
        kCVPixelBufferWidthKey as String: W, kCVPixelBufferHeightKey as String: H
    ])
writer.add(entrada)
writer.startWriting()
writer.startSession(atSourceTime: .zero)

func buffer(_ cg: CGImage) -> CVPixelBuffer {
    var pb: CVPixelBuffer?
    CVPixelBufferCreate(kCFAllocatorDefault, W, H, kCVPixelFormatType_32ARGB, nil, &pb)
    CVPixelBufferLockBaseAddress(pb!, [])
    let ctx = CGContext(data: CVPixelBufferGetBaseAddress(pb!), width: W, height: H,
        bitsPerComponent: 8, bytesPerRow: CVPixelBufferGetBytesPerRow(pb!),
        space: CGColorSpaceCreateDeviceRGB(),
        bitmapInfo: CGImageAlphaInfo.noneSkipFirst.rawValue)!
    ctx.draw(cg, in: CGRect(x: 0, y: 0, width: W, height: H))
    CVPixelBufferUnlockBaseAddress(pb!, [])
    return pb!
}

var i: Int64 = 0
for nombre in archivos {
    guard let img = NSImage(contentsOfFile: "\(carpeta)/\(nombre)") else { continue }
    var r = NSRect(origin: .zero, size: img.size)
    guard let cg = img.cgImage(forProposedRect: &r, context: nil, hints: nil) else { continue }
    while !entrada.isReadyForMoreMediaData { usleep(2000) }
    adaptador.append(buffer(cg), withPresentationTime: CMTime(value: i, timescale: fps))
    i += 1
}
entrada.markAsFinished()
let sem = DispatchSemaphore(value: 0)
writer.finishWriting { sem.signal() }
sem.wait()
print("listo: \(archivos.count) cuadros a \(fps) fps")
