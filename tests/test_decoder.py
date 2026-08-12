from services.scrfd_decoder import SCRFDDecoder

decoder = SCRFDDecoder()

anchors = decoder.generate_anchors(height=80, width=80, stride=8)

print("Anchor Shape:", anchors.shape)
print(anchors[:10])

print("\nTesting bbox decoder...")
decoder.test_bbox_decoder()
