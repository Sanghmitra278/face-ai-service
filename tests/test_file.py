import onnx

model = onnx.load("onnx/scrfd_500m_bnkps.onnx")

print("IR Version:", model.ir_version)

print("\nInputs:")
for i in model.graph.input:
    print(i.name)

print("\nOutputs:")
for o in model.graph.output:
    print(o.name)

print("\nNodes:", len(model.graph.node))
