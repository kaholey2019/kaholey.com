ObjC.import("Vision");
ObjC.import("Foundation");

function analyze(path) {
  const url = $.NSURL.fileURLWithPath(path);
  const handler = $.VNImageRequestHandler.alloc.initWithURLOptions(url, $.NSDictionary.dictionary);
  const request = $.VNClassifyImageRequest.alloc.init;
  const error = Ref();
  const ok = handler.performRequestsError(ObjC.wrap([request]), error);
  if (!ok) {
    return { path: path, error: String(error) };
  }

  const observations = ObjC.unwrap(request.results);
  const tags = observations.map((item) => ({
    label: item.identifier.js,
    confidence: item.confidence,
  }));
  tags.sort((a, b) => b.confidence - a.confidence);
  return { path: path, tags: tags.slice(0, 5) };
}

function run(argv) {
  const paths = argv;
  const out = paths.map(analyze);
  return JSON.stringify(out, null, 2);
}
