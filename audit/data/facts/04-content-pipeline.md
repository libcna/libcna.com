# Fact sheet 04: content loading, XNB, CNB, Content Pipeline, models, glTF

Scope: CNA TARGET `009d40f5dd085c4e674d3479675fac84b12b3e0a` (read-only worktree
`/rv/tmp/libcna-v2/cna-target`), compared with BASE `1bb2145d99ed572dd4eb15009c34e2e5f410fcf0`
(`/rv/tmp/libcna-v2/cna-base`, the revision the site was last synchronised to). All citations are
TARGET-relative `path:line` unless prefixed `BASE:`. No compiler, CMake or CNA binary was run; every
claim is from reading files. Nothing under `/tmp` was built.

Evidence tags used below (highest to lowest, as required by the audit rules):

| Tag | Meaning |
|---|---|
| `[impl]` | read directly in implementation source |
| `[cmake]` | build configuration or header contract |
| `[test]` | asserted by a committed test or fixture (test existence read, not executed) |
| `[gen]` | CNA generated report (`docs/*-report.md`, produced by scripts from JSON); counts re-checked where stated |
| `[md]` | CNA hand-written Markdown. UNTRUSTED. Used for orientation, and quoted only where flagged |
| `[site]` | current libcna.com page (old claim being checked) |

Where a fact rests on `[md]` or `[gen]` alone it says so; the website must hedge such statements
("CNA reports ...") rather than assert them.

---

## Verified facts

Headline list. Details and citations are in the later sections.

| # | Fact | Evidence |
|---|---|---|
| V1 | **CNA now authors compiled content.** A build-time tool `cna-content` (CMake target `cna_content_tool`, `OUTPUT_NAME "cna-content"`) turns source files into `.cnb` (default) or `.xnb`. The BASE claim "CNA only reads .xnb, never writes it" is false at TARGET. | `cmake/ToolContentPipeline.cmake:17-21`; `tools/content/content.cpp:283-372`; `modules/content/src/Xnb/XnbWriter.cpp`, `XnbAssetTypeWriters.cpp:827-1340` |
| V2 | **A new binary format, CNB (`.cnb`), exists**: 64-byte header, 48-byte table-of-contents entries, CRC-32C per structure and per chunk, container 1.0. Not present at BASE. | `modules/content/include/CNA/Content/Cnb/CnbFormat.hpp:71-96`; `modules/content/src/Cnb/*.cpp` |
| V3 | `ContentManager::Load<T>` resolution ladder is now **`.xnb`, then `.cnb`, then a literal `.cnb` name, then the per-type loose reader (literal path, `.cnj`, reader extensions)**. BASE had no `.cnb` tier. | `modules/content/include/Microsoft/Xna/Framework/Content/ContentManager.hpp:494-568` |
| V4 | Built-in XNB type readers: **61** registered names (60 where `SHARP_RUNTIME_HAS_NATIVE_INT128` is not set, because `DecimalReader` is conditional). BASE was 50 (49 without FFmpeg). The Video reader is no longer FFmpeg-conditional. | reader table below; `modules/content/src/Xnb/XnbBuiltInReaders.cpp:24-43`; `DecimalDateTimeContentTypeReaders.cpp:12-15`; `BASE: modules/content/src/Xnb/XnbBuiltInReaders.cpp:39-41` |
| V5 | **`Game`'s constructor now calls `RegisterAllBuiltInXnbReaders()`.** "Built-in readers must be registered explicitly at startup" is no longer true for a `Game` subclass. It is still true for a `ContentManager` used without a `Game` (tools, tests, C API). | `modules/runtime/src/Game.cpp:333-338`; BASE has no call site outside `tools/audio` |
| V6 | `ResourceContentManager` is **implemented** (no longer a stub): resource-family `OpenStream`. Its base `Load<T>` does not route through `OpenStream`; `ReadAsset<T>` is a protected seam. | `modules/content/src/Xna/ResourceContentManager.cpp:12-77`; `BASE: .../ResourceContentManager.cpp:12-16` (`CNA_STUB`) |
| V7 | Custom `.xnb` types: `ContentTypeReader<T>` + `ContentTypeReaderManager::AddTypeCreator` existed at BASE. New: `ReflectiveTypeReaderBuilder<T>` (declare the field list once, `.Register()`/`.RegisterShared()`), `EnumTypeReader<TEnum>`, five `ContentSerializer*Attribute` descriptors. The site's "no ReflectiveReader, custom types cannot be loaded from .xnb" needs rewording. | `Microsoft/Xna/Framework/Content/ReflectiveTypeReader.hpp:289,355-554`; `git diff --stat` file list of `.../Content/` headers |
| V8 | Runtime glTF (`.gltf`/`.glb` via `Load<Model>`) at TARGET: **all mesh groups imported into one `Model`**, every skin in `Model::SkinsEXT`, **unit scale hard-coded 1.0**, rigid node animation kept (`ModelAnimationsEXT`) for unskinned models and **dropped with a diagnostic only when skins occupy `Model::Tag`**, factor-only PBR kept, `extensionsRequired` **is enforced** by a 21-record registry. Same as the alpha.1 site text; no regression, small additions (legacy `_TANGENT/_BINORMAL`, material-extension factor carriage). | `ContentManager.cpp:2881-3245,3084,3221,3569,4011,4252`; `GltfImportCore.cpp:4583-4700,5176-5187,2800-2862` |
| V9 | CNA tool executables at TARGET: `cna-content`, `cna_tool_gltf_to_cnj`, `cna_tool_gltf_to_cnb`, `cna_tool_cnj_to_cnb`, `cna_tool_source_to_cnb`, `cna_tool_cnb_info`, `cna_tool_xnb_interop_fixtures`. BASE had only `cna_tool_gltf_to_cnj`. All are built by default (no option gate). | `CMakeLists.txt:391-399`; `cmake/Tool*.cmake` |
| V10 | The compile-in switch for the Content Pipeline does not exist: `modules/content` and `modules/content-pipeline` are always added; only optional **inputs** are switchable (FreeType, FFmpeg, zlib, zstd, Draco, external `fxc`). | `modules/CMakeLists.txt:352-355`; `modules/content-pipeline/CMakeLists.txt` |
| V11 | CNB chunk compression exists (Zstandard, opt-in per chunk, off by default) **but only through `CnbWriter::SetCompression` (library) and the C ABI**. No built-in codec, no `cna-content` option and no standalone tool ever enables it. | `Cnb/CnbWriter.cpp:180-190`; grep of non-test `SetCompression(` callers = `CnaCApiCnb.cpp:2882` only |
| V12 | CNB memory mapping is **not implemented**; CNA measured it and decided against it (reads whole file, verifies every CRC). | `Cnb/CnbDocument.cpp:412-448`; `Cnb/CnbCrc32c.cpp:9-13`; `docs/cnb-mmap-measurements.md` `[md]` |
| V13 | Test counts (method: `grep -oE '\b(TEST\|TEST_F\|TEST_P\|TYPED_TEST\|TYPED_TEST_P)\s*\(' -r <dir> --include=*.cpp --include=*.hpp`, reproduces the site's 978 at BASE): `modules/content/tests` BASE 112 sources / 978; TARGET **170 sources / 1872**; new `modules/content-pipeline/tests` **47 sources / 487**. | counted 2026-09-24 |
| V14 | Compiled D3D9 Effect Framework bytecode (`EffectReader`, `Effect(device, bytes)`): FNA3D plus **nine** opt-in CMake options, all default OFF (EasyGL, Vulkan, WebGPU, Software, DirectX 9, 11, 12, SDL_GPU, OpenGL4). BASE had three options (EasyGL, Vulkan, SDL_GPU). Renderer agent owns the per-renderer verdict. | `cmake/RendererSelection.cmake:310,331,352,380,401,416,455,495,519` |
| V15 | The experimental C ABI now exports CNB (`cnb.h`, 272 `cna_cnb_*` functions), content readers (`content_readers.h`) and a manifest/reader-usage surface; ABI version 0.29.0 (BASE 0.7.0). The Content **Pipeline** has no C ABI export. | `modules/c-api/include/CNA/C/cnb.h`, `content.h`, `abi.h:37`; `docs/content-pipeline.md:1250` `[md]` |

---

## Content Pipeline (what exists)

### Module and build structure

* `modules/content` (`cna_content`): runtime `ContentManager`, XNB reader **and writer** (`CNA::Internal::Xnb`),
  CNB codecs (`CNA::Content::Cnb`), the canonical pipeline engine (`CNA::Content::Pipeline`:
  `ContentImporter`, `ContentProcessor`, `ContentTypeWriter`, `ContentPipelineRegistry`, `ContentPipeline`,
  manifest, configuration). `modules/content/CMakeLists.txt:1-36`. A game that only loads content links this.
* `modules/content-pipeline` (`cna_content_pipeline`): build-time-only code (FreeType `.spritefont`,
  block-compression encoder, FBX/`.x` readers, XNA `Microsoft::Xna::Framework::Content::Pipeline` façade,
  effect-compiler and XMA-encoder services). Only `cna_content_compiler` links it, so FreeType/FFmpeg never enter a
  runtime game's link closure. `modules/content-pipeline/CMakeLists.txt:1-11`; `cmake/ToolContentPipeline.cmake:4-16`.
  Size: about 28k lines of `.cpp` in `modules/content-pipeline`; `tools/content/content.cpp` is 3392 lines.
* Targets: `cna_content_compiler` (static library, alias `CNA::ContentCompiler`) carries the whole command
  coordinator; `cna_content_tool` (`cna-content`) is a 42-line `main`; examples
  `cna_custom_content_compiler_example` (`modules/content/examples/custom-content-compiler.cpp`) and
  `cna_xna_custom_pipeline_example` (`modules/content-pipeline/examples/xna-custom-pipeline.cpp`) are built only under
  `CNA_BUILD_EXAMPLES` or `CNA_BUILD_TESTS`. `cmake/ToolContentPipeline.cmake:4-52`.
* Optional inputs (all three-state `OFF/AUTO/ON` unless noted):
  * `CNA_ENABLE_FONT_PIPELINE` (default `AUTO`, FreeType) gates the `.spritefont` route. `CMakeLists.txt:105-107`; `modules/content-pipeline/CMakeLists.txt:17-45`. Without it a `.spritefont` build fails with a message saying so.
  * `CNA_ENABLE_MEDIA_PIPELINE` (default `AUTO`, needs FFmpeg libs) gates build-time `.mp3`/`.wma`/`.wmv` decoding. `modules/content-pipeline/CMakeLists.txt:47-83`.
  * zlib (found automatically) enables compressed arrays in binary FBX. `modules/content-pipeline/CMakeLists.txt:85-99`.
  * `CNA_CNB_ZSTD` (default `AUTO`, libzstd) enables Zstandard chunks in CNB. `modules/CMakeLists.txt:92-126`.
  * `CNA_ENABLE_DRACO` (default ON, OFF under Emscripten) for `KHR_draco_mesh_compression`. `modules/CMakeLists.txt:128-141`.
  * `CNA_FXC_EXECUTABLE` / `CNA_FXC_LAUNCHER` cache strings bake a default external HLSL compiler. `modules/content-pipeline/CMakeLists.txt:100-122`.
  * `CNA_ENABLE_VIDEO` (FFmpeg for runtime video playback) is separate from the pipeline. `modules/CMakeLists.txt:9-57`.

### CLI: `cna-content`

Usage text `[impl]` `tools/content/content.cpp:283-372`:

```text
cna-content build <source-file | source-directory | .contentproj> -o|--output <output>
    [--format cnb|xnb] [--config <file>] [--workers <1..64>]
    [--xnb-platform <name>] [--xnb-version 4|5] [--xnb-profile reach|hidef]
    [--xnb-compress none|lzx|lz4] [--xnb-reader-names xna40|portable] [--xnb-allow-unverified-xbox]
    [--fx-compiler <path>] [--fx-compiler-launcher <program>]
    [--xma-encoder <path>] [--xma-encoder-launcher <program>] [--xma-encoder-arg <arg>]...
    [--font-directory <dir>]... [--build-configuration <name>]
    [--explain] [--quiet] [--xna-compatible] [--only-configured-assets]
cna-content clean <output-directory> [--quiet]
```

* Default format is CNB. A single-file build needs an output path whose extension matches `--format`; a directory
  build needs an output directory and preserves relative logical names (`content.cpp:308-311`).
* `--workers` accepts 1 to 64 (`content.cpp:374-387`); 1 is the default serial mode.
* `--xnb-platform` names: `windows`, `windowsphone`, `xbox360` (XNA 4.0 targets) and `desktopgl`, `linux`, `ios`,
  `android`, `windowsgl` (not XNA 4.0 targets). `modules/content/src/Xnb/XnbFileOptions.cpp:22-29`.
  `xbox360` is refused unless `--xnb-allow-unverified-xbox` (`content.cpp:316-320,518-524`).
* `--xnb-compress lz4` is refused on an XNA 4.0 target platform (`XnbFileOptions.cpp:114`, `content.cpp:321-331`).
* `--xna-compatible` switches three refusals into XNA-style warnings (unknown/unconvertible processor parameter,
  glyph missing from a font). `docs/content-pipeline.md:117-138` `[md]` matches `content.cpp:454-462` `[impl]`.
* Incremental state: `.cna-content-manifest.json` (**manifest version 9**, `ContentBuildManifest.hpp:15`, file name
  `:19`), lock file `.cna-content.lock` (`tools/common/CnaContentStaging.hpp:37`). Optional strict config
  `.cna-content.json` (`ContentBuildConfiguration.hpp:18`). `docs/content-pipeline.md` says "version 8" in places: stale.
* `.cna-content.json` root keys are exactly `format` (`"CNA.ContentPipeline.Config"`), `version` (1), `outputFormat`,
  `sourceRoots`, `assets`; per-asset keys `logicalName`, `importer`, `processor`, `writer`, `outputFormat`,
  `parameters` (typed `bool|i64|u64|f64|string`). `Pipeline/ContentBuildConfiguration.cpp:24,206,277`.
  (`outputFormat` is not in the doc's example; it is real.)

### CMake integration

`cna_add_content(TARGET <t> (SOURCE_DIR <d> | CONTENT_PROJECT <x.contentproj>) OUTPUT_DIR <d> [CONFIG_FILE <f>] [WORKERS <1..64>]
[FORMAT cnb|xnb] [XNB_PLATFORM ...] [XNB_PROFILE ...] [XNB_COMPRESS ...] [XNA_COMPATIBLE] [QUIET] [CONTENT_EXECUTABLE <path>])`
`[cmake]` `cmake/ToolContentPipeline.cmake:67-237`. It creates an `add_custom_target` that runs `cna-content build ...`
every time the target is requested (the manifest makes an unchanged run a cheap no-op). `CONTENT_PROJECT` refuses
`FORMAT`, `XNB_*`, `CONFIG_FILE` and `XNA_COMPATIBLE` (`:130-141`). Cross-compiling requires an explicit host
`CONTENT_EXECUTABLE` (`:182-185`). `XNB_*` options need `FORMAT xnb` (`:152-157`).

### Built-in routes (what a source becomes)

Registered in `RegisterBuiltInContentPipeline` (`tools/content/content.cpp:3310-3360`). Source extensions read from
each importer's `SourceExtensions()`:

| Source | Importer route (source file) | `.cnb` | `.xnb` |
|---|---|---|---|
| `.png .jpg .jpeg .bmp .tga .gif .psd .hdr .pic .pnm` | image importer + `TextureProcessor` (`Pipeline/Texture2DContentPipeline.cpp`) | Texture2D, **Rgba8 only** | Texture2D |
| `.wav` | `Pipeline/SoundEffectContentPipeline.cpp:31` | SoundEffect (Pcm16, or Pcm8 in schema 2) | SoundEffect |
| `.mp3 .wma` as decoded SoundEffect | `SoundEffectContentPipeline.cpp:233` (needs media pipeline) | yes | yes |
| `.mp3 .ogg .oga .qoa .flac .opus .aac .wma` | `Pipeline/SongContentPipeline.cpp:87` streaming reference, media file deployed beside the `.cnb` | Song (metadata + reference) | Song |
| `.mp4 .ogv .webm .mkv .avi .mov` | `Pipeline/VideoContentPipeline.cpp` (frame size/fps must be configured) | Video (metadata + reference) | Video |
| `.gltf .glb` | `Pipeline/ModelContentPipeline.cpp:247` | Model schema 1 (one primary; `generateChildAssets` opt-in for multi-group) | Model, **skeleton/animations/morphs/lights dropped with warnings**, PBR downgraded to stock effects |
| `.cnj` (typed) | `Pipeline/CnjContentPipeline.cpp:154` | Texture2D/3D, TextureCube, SpriteFont, SoundEffect, Curve, AnimationClip, Model | same, where the XNB writer supports it |
| `.xnb` (supported built-in root) | `Pipeline/XnbContentPipeline.cpp:240` | transcoded to native CNB | not written (`.xnb` is a source here) |
| `.spritefont` | `content-pipeline/src/SpriteFontContentPipeline.cpp:1268` (FreeType) | SpriteFont | SpriteFont (atlas DXT3 when `.xnb`) |
| `.fxb` (compiled effect) | `Pipeline/EffectContentPipeline.cpp:76` | **no** (CNB has no Effect schema) | Effect |
| `.fx` (HLSL source) | `content-pipeline/src/EffectSourceContentPipeline.cpp:327`, external `fxc` | **no** | Effect, only with an external `fxc` |
| `.x` | `content-pipeline/src/XnaModelSourceContentPipeline.cpp:157` | Model via XNA `ModelProcessor` | Model |
| `.fbx` | `XnaModelSourceContentPipeline.cpp:187` | Model | Model |
| `.xml` (XNA intermediate XML) | `content-pipeline/src/XnaXmlSourceContentPipeline.cpp:79` | **refused** (no CNB schema for arbitrary graphs) | any type registered with the XNA `ContentCompiler` |
| `.contentproj` | `Microsoft/Xna/Framework/Content/Pipeline/Tasks/ContentProject.hpp`, `BuildContent.hpp` (read as MSBuild-free XML; Compile/Content/None items, `<Importer>/<Processor>/<ProcessorParameters_*>`, platform, profile, compress) | via project | via project |

Row-level verification: the `.x/.fbx -> .cnb` leg and the DXT-in-CNB behaviour are `[impl]`/comment-level only
(`XnaModelSourceContentPipeline.hpp:1-40`: "the canonical processed model both writers already take"). The `.mp3/.wma` row
depends on `CNA_ENABLE_MEDIA_PIPELINE`.

Texture processor parameters (`[impl]` `Pipeline/Texture2DContentPipeline.cpp:78-135,1104`): `colorKey` (string `R,G,B`),
`textureFormat` (`NoChange|Color|DxtCompressed|Dxt1|Dxt3|Dxt5`), `generateMipmaps`, `premultiplyAlpha` (**default true**),
`resizeToPowerOfTwo`. A CNB build that requests DXT keeps uncompressed Rgba8 and warns
(`Texture2DContentPipeline.cpp:1412-1415`; codec refuses non-Rgba8: `Cnb/CnbTextureCodec.cpp:183-185`).
Model processor: bool `generateChildAssets`, glTF only (`ModelContentPipeline.cpp:111,370-399`).

### XNA Content Pipeline façade (`Microsoft::Xna::Framework::Content::Pipeline`)

`[impl]` 107 public headers under `modules/content-pipeline/include/Microsoft/Xna/Framework/Content/Pipeline/`,
implemented in `modules/content-pipeline/src/Xna/` (about 24k lines in that tree). It is a view over the canonical
engine, not a second engine (`docs/xna-content-pipeline-compat-api.md:1-30` `[md]`).

* Importers with implementation files (10): `TextureImporter`, `WavImporter`, `Mp3Importer`, `WmaImporter`, `WmvImporter`,
  `EffectImporter`, `FontDescriptionImporter`, `XImporter`, `FbxImporter`, `XmlImporter`
  (`modules/content-pipeline/src/Xna/*Importer.cpp`).
* Processors: `TextureProcessor`, `SpriteTextureProcessor`, `ModelTextureProcessor`, `MaterialProcessor`,
  `ModelProcessor`, `EffectProcessor`, `FontDescriptionProcessor`, `FontTextureProcessor`, `SongProcessor`,
  `SoundEffectProcessor`, `VideoProcessor`, `PassThroughProcessor` (`src/Xna/Processors/*.cpp`).
* Serialization: `IntermediateSerializer` / `IntermediateReader` / `IntermediateWriter` (XNA intermediate XML) and
  `ContentCompiler` / `ContentWriter` / `ContentTypeWriter` (`src/Xna/Serialization/**`).
* Tasks: `BuildContent`, `CleanContent`, `BuildXact` (declared, HOST_SUBSTITUTION), `ContentProject`
  (`src/Xna/Tasks/*.cpp`).
* Registering your own component: `RegisterXnaImporter<T>(registry, name, attribute, version)` /
  `RegisterXnaProcessor<T>` (`docs/xna-content-pipeline-compat-api.md` §4 `[md]`; the templates are in
  `Microsoft/Xna/Framework/Content/Pipeline/` headers). Assembly scanning has no C++ equivalent (`PipelineComponentScanner`
  enumerates registry contents).
* `[gen]` `docs/xna-content-pipeline-parity-report.md:9-27` (generated by `tools/xna-pipeline-oracle/parity_report.py`
  from `tests/reference/xna40/content-pipeline-api.json`): 128/128 public types, 705/705 members, 27/27 enum values,
  10/10 importers, 12/12 processors, 47/47 processor properties, 18/18 source extensions `IMPLEMENTED+TESTED`, 0 missing.
  Status vocabulary includes `SEMANTIC_EQUIVALENT` (79 types) and `HOST_SUBSTITUTION` (5 types: `PipelineComponentScanner`,
  `BuildContent`, `BuildXact`, `CleanContent`, `GetLastOutputs`; exception serialization members). I confirmed the
  implementation files exist for all 10 importers and all processors; I did **not** re-verify the "matches the genuine
  XNA 4.0 importer, measured under Wine" statements in that report.
* Caveats CNA states in the same report: `.wma`/`.wmv` importers "could not be measured" against the genuine runtime
  (no Windows Media runtime in Wine), `.mp3` measured on Windows only; `.fx` route verified with Microsoft's legacy
  `fxc` (June 2010 DirectX SDK) through Wine; Phone and Xbox target legs `UNVERIFIED`; `.wav` for Xbox reports
  `XMA ENCODER EXTERNALLY UNAVAILABLE` (`docs/xna-content-pipeline-parity-report.md:256-278`).
* `[impl]` XMA: `cna-content` ships no XMA encoder; `--xma-encoder` attaches an external one (`content.cpp:349-360`).
* The custom-component API is **explicitly experimental**: `ContentPipelineExtensionApiIsExperimental = true`
  (`modules/content/include/CNA/Content/Pipeline/ContentPipeline.hpp:98`), a source/toolchain compatibility model, not a plugin
  ABI (`docs/content-pipeline.md:980-1050` `[md]`).

### XNB writing (re-verification of the BASE claim "CNA cannot author XNB")

`[impl]` **CNA writes XNB.** Evidence: `modules/content/src/Xnb/XnbWriter.cpp`, `XnbByteWriter.cpp`, `XnbCompressionWriter.cpp`,
`LzxEncoder.cpp`, `XnbTypeWriterRegistry.cpp`; public entry `WriteXnbAsset` (`include/CNA/Internal/Xnb/XnbAssetWriter.hpp:49`),
`WriteXnbAssetFile` (`:111`).

* Writers registered for: Texture2D, Texture3D, TextureCube, SpriteFont, SoundEffect, Song, Video, VertexDeclaration,
  VertexBuffer, IndexBuffer, BasicEffect, AlphaTestEffect, DualTextureEffect, EnvironmentMapEffect, SkinnedEffect,
  compiled `Effect`, external reference, effect parameter table, EffectMaterial, Model
  (`Xnb/XnbAssetTypeWriters.cpp:829,863,898,932,1008,1046,1066,1080,1091,1129,1164,1181,1196,1210,1227,1243,1270,1284,1317,1337`),
  plus primitives, math types, Curve and closed collections (`Xnb/XnbBuiltInWriters.cpp:463-540`:
  `List<String|Int32|Char|Rectangle|Vector3|Matrix>`, `Dictionary<String,Int32|String>` in three spellings, `Vector3[]`).
* Container options (`XnbFileOptions.hpp`): platform (8 names above), version 4 or 5 (default 5), profile Reach/HiDef
  (default Reach), compression None/LZX/LZ4 (default None), reader-name style `xna40` (default) or `portable`.
* Encoder facts: LZX is a real encoder, one verbatim block per 32 KiB frame, deterministic (`docs/xnb-interoperability.md`
  §2.1.1 `[md]`, `Xnb/LzxEncoder.cpp` `[impl]`, 38 KB). LZ4 is a raw single block. `tests/interop/xna40/README.md` `[md]` says a five-byte
  trailer after the final LZX block was needed before genuine XNA loaded CNA's compressed files, and that
  `LzxEncoderTest.EveryCompressedPayloadEndsWithTheTrailerXnaRequires` now pins it.
* glTF to XNB Model drops data with named warnings: skeleton, animation clips, lights, morph targets, generated child
  assets are refused, PBR effects are downgraded to the corresponding stock effect, an external-effect part is refused
  (`modules/content/src/Pipeline/XnbOutputContentPipeline.cpp:424-470,728-760,838-847,1390-1425`).
* Xbox 360: the writer converts the SoundEffect WAVEFORMATEX and, per `XboxByteSwapUnit`, Texture2D/3D/Cube and SpriteFont atlas
  payloads for formats with a measured swap unit (`XnbAssetTypeWriters.cpp:829-930,932-950`); any other format is refused; the
  platform itself is refused by default (`XnbFileOptions.cpp:24`). CLI help and `docs/xnb-interoperability.md` §2.2 still say only the
  WAVEFORMATEX is converted: stale relative to the code.
* Verification status as CNA reports it `[md]`, to be attributed, not asserted:
  * byte-identical to genuine XNA 4.0 output for `List<string>` and to MonoGame output for a Texture2D and a SoundEffect
    (`docs/xnb-interoperability.md` §4; tests `XnbWriterTest.Golden*`).
  * "Executed against a genuine Microsoft XNA 4.0 runtime on 2026-09-06 ... six of six uncompressed fixtures loaded ...
    LZX corpus now passes six of six", host Debian + Wine + DXVK (`tests/interop/xna40/README.md:1-40`).
  * **Contradiction inside CNA's own docs**: `docs/xnb-interoperability.md` (last edit 2026-09-03) still says "Nothing has this label
    yet ... never been run against a real XNA runtime"; the README (2026-09-06) and CLI help
    (`content.cpp:321-331`) say it was. Later dated wins, but see Open questions.
  * The independent conformance parser is `tools/xnb/xnb_conformance.py` (shares no code with CNA).

### Not supported / boundaries (verified where cited)

* No embedded HLSL compiler; `.fx` needs an external `fxc`-compatible program (`content.cpp:332-337`; `docs/content-pipeline.md:412-470`).
* No `.cnb` for Effect or arbitrary `.xml` graphs.
* `cna-content` does not expose CNB chunk compression (V11).
* No Content Pipeline C ABI (`docs/content-pipeline.md:1250` `[md]`).
* The XNB output path cannot write generated glTF child assets (`XnbOutputContentPipeline.cpp:439-445`).
* glTF pipeline route: `generateChildAssets` is required for multi-group files; other scenes than the default are not imported; named
  source roots are not honoured for glTF URI loading (`docs/content-pipeline.md:472-514,626-633` `[md]`; the
  multi-group refusal text is `ModelContentPipeline.cpp:391-399` `[impl]`).
* Benchmarks in `docs/content-pipeline-benchmark.md` are single-host, Debug-build developer evidence ("not a released
  performance guarantee"): do not quote as guarantees.

---

## CNB

**What it is** `[impl]`: CNA's own compiled runtime container, one asset per file, deterministic, little-endian, no host-ABI
dependence. It is a **CNA output format**, not XNB and not a package/archive. Authoritative spec is `docs/cnb-format.md`
(`[md]`, but CNA says a conformance test compares its constants to the code:
`modules/content/tests/CNA/Content/Cnb/CnbSpecConformanceTests.cpp`; existence confirmed).

| Item | Value | Evidence |
|---|---|---|
| Magic | `43 4E 42 1A` (`"CNB"` + 0x1A) | `CnbFormat.hpp:74` |
| Container version | major 1, minor 0 (minor bumps additive; major != 1 rejected) | `CnbFormat.hpp:92-95`; `docs/cnb-format.md` §6 |
| Header | 64 bytes; header CRC covers bytes [0,44) at offset 44; 16 reserved zero bytes | `CnbFormat.hpp:77-89` |
| TOC entry | 48 bytes: type, flags (bit0 Mandatory), offset, storedSize, uncompressedSize, CRC-32C, compression, alignment, reserved | `CnbFormat.hpp:80`; `CnbDocument.hpp:16-55` |
| Checksums | CRC-32C for header, TOC and each chunk (of stored bytes); hardware CRC (SSE4.2, ARMv8) picked at runtime | `Cnb/CnbCrc32c.cpp:73-128` |
| Chunk ids | four printable ASCII bytes; uppercase first byte reserved for CNA (convention, not enforced) | `CnbFormat.hpp:111-160`; `docs/cnb-format.md` §5 |
| Container chunks | `CMET` (type name + content name; **required for custom types**), `XREF` (mandatory, external logical names, validated by `CnbLogicalNameProblem`) | `CnbFormat.hpp:320-346` |
| Asset type ids | 1 Texture2D, 2 Texture3D, 3 TextureCube, 4 SpriteFont, 5 Model, 6 AnimationClip, 7 Curve, 8 SoundEffect, 9 Song, 10 Video, 11 Effect (**reserved, no schema, by design**); 0x40000000+ reserved; 0x80000000+ game-defined via `CnbAssetTypeIdFromName` (FNV-1a-32 OR 0x80000000) | `CnbFormat.hpp:232-275` |
| Schema versions | Texture 1, SpriteFont 1, Model **1 and 2**, AnimationClip 1, Curve 1, SoundEffect **2** (v1 files still read), Song/Video 1 | `Cnb/Cnb*Codec.hpp` (`CnbTextureSchemaVersion` etc.) |
| Compression codecs | wire ids 0 None, 1 LZ4 (id only), 2 Zstandard, 3 Deflate (id only). **Only None and Zstd (when built with libzstd) are implemented.** Off by default, per chunk. | `CnbFormat.hpp:182-215`; `Cnb/CnbChunkCompression.cpp:26-60` |
| Read limits (defaults) | file 512 MiB, chunk count 65536, chunk 384 MiB, total uncompressed 1 GiB, string 1 MiB, array 16 Mi elements, alignment 4096 | `CnbReadLimits.hpp:22-60` |
| Determinism | same inputs give identical bytes, asserted across processes | `docs/cnb-format.md` §13,15.2 `[md]` |
| Load path | `ContentManager::Load<T>` → `CnbDocument::ParseFile` (reads the **whole file** with `ifstream`, validates every invariant) → `CnbLoaderRegistry::ResolveForDocument` → typed decoder | `ContentManager.hpp:527-549,661-691`; `Cnb/CnbDocument.cpp:412-448` |
| Built-in loaders | Texture2D/3D/Cube, SpriteFont, Model (v1/v2), SoundEffect, Song, Video (`ContentManager::RegisterBuiltinLoaders`); Curve and AnimationClip (`CnbLoaderRegistry::RegisterBuiltIns`) | `ContentManager.cpp:6323-6416`; `Cnb/CnbLoaderRegistry.cpp:245-262` |
| Custom types | `ContentManager::RegisterCnbLoaderEXT<T>(id, canonicalName, factory)`: custom-range only, name must hash to id; registration is process-wide | `ContentManager.hpp:440-458` |
| Media | Song/Video carry metadata + a streaming reference, never the media; `cna-content` deploys a byte-identical media copy | `docs/content-pipeline.md:516-566` `[md]` |
| Texture payloads | schema 1 **encodes Rgba8 only**; reader accepts descriptors for other formats but no writer produces them | `Cnb/CnbTextureCodec.cpp:183-185`; `CnbTextureCodec.hpp:1-60` |

**Relation to XNB and CNJ.** CNB shares no code with XNB and has no reader tables, reflection or platform byte
(`docs/cnb-format.md` §1 `[md]`, consistent with the code layout). CNJ (`.cnj`, JSON plus binary sidecars) remains a supported
authoring/intermediate format loaded by loose readers and is an *input* to `cna_tool_cnj_to_cnb` and `cna-content`.
`.xnb` is a *source* for `cna-content` (`XnbImporter`) and the format `--format xnb` writes.

**Model schema 1 does not carry** glTF material variants (the `.cnj -> .cnb` compiler refuses them,
`Cnb/CnbModelFromCnj.cpp:491-499,662-667`) or the import report or cameras (no camera field in
`Cnb/CnbModelData.hpp`; `BuildModelFromCnbEXT` restores lights, morph data, skeleton and clips, `ContentManager.cpp:5255+`).
Direct runtime glTF loading does set `CamerasEXT`, `SkinsEXT` and the import report (`ContentManager.cpp:4212,4291,4293`).

**Tooling to create/inspect CNB** `[impl]`:

* `cna-content build <src> -o <out>` (default format).
* `cna_tool_cnj_to_cnb <input.cnj> [output.cnb] [--content-root <dir>] [--name <logical>] [--quiet]` (`tools/cnj_to_cnb/cnj_to_cnb.cpp:25-64`).
* `cna_tool_gltf_to_cnb <input.gltf|glb> <outputDir> <baseName> [--unit-scale <f>] [--keep-cnj <dir>] [--quiet]` (`tools/gltf_to_cnb/gltf_to_cnb.cpp:89-140`).
* `cna_tool_source_to_cnb <input> <output.cnb> [--name] [--mipmaps] [--mip-color-space linear|srgb] [--color-key R,G,B] [--as texture2d|soundeffect|song|texturecube|video] [--stream] [--duration-ms] [--title] [--frame-size WxH] [--fps] [--soundtrack 0..2] [--quiet]` (`tools/source_to_cnb/source_to_cnb.cpp:60-125`).
* `cna_tool_cnb_info <file.cnb> [--refs] [--chunks] [--quiet]` validates and prints, exit code non-zero when malformed (`tools/cnb_info/cnb_info.cpp:38-56`).

**Measurements** (`[md]`, single machine: AMD, NVMe, Debian 13, gcc `-O2`, 2026-08-27; probes committed at
`spikes/cnb-compression-spike/measure.cpp` and `spikes/cnb-mmap-spike/measure.cpp`, so *reproducible*, not portable):
zstd-3 ratio 51 % (1024x1024 photo Rgba8), 57 % (normal map), 27 % (2 s Pcm16), 15 % (vertex bytes), 28 % (indices);
decompress 932 / 2007 / 1264 MB/s; compression only saves load time when the device reads below 456 / 1469 / 1073 MB/s
(texture / audio / vertex), measured NVMe 2.5 to 4.4 GB/s, so **compression slows loading on NVMe**; mmap saves 4.7 ms of a
32 MiB load while CRC verification cost 62.5 ms, so hardware CRC-32C was implemented (127.3 ms to 19.8 ms end to end) and
mmap "measured and rejected" (`docs/cnb-compression-measurements.md`, `docs/cnb-mmap-measurements.md`). State these as
CNA-reported developer measurements, never as guarantees.

---

## XNB readers

### Registration model

* Registry is process-wide (`ContentTypeReaderManager::AddTypeCreator`, first registration wins; repeat is ignored).
  `Microsoft/Xna/Framework/Content/ContentTypeReaderManager.hpp:36-52`.
* `CNA::Internal::Xnb::RegisterAllBuiltInXnbReaders()` (`include/CNA/Internal/Xnb/XnbBuiltInReaders.hpp:38`, still under
  `Internal`; the site's include path `CNA/Internal/Xnb/XnbReaderRegistry.hpp` **does not exist**, the header is
  `XnbBuiltInReaders.hpp`) registers everything in the table below. Idempotent.
* **Auto-registration at TARGET**: `Game::Game()` calls it (`modules/runtime/src/Game.cpp:333-338`, comment: "make every XNA game
  ready to load built-in XNB types before Initialize()/LoadContent() can run"). A standalone `ContentManager` does not
  (the header comment `XnbBuiltInReaders.hpp:5-16` still says so and is correct for that case).

### Reader list (61 registered canonical names; from every `AddTypeCreator` call under `modules/content/src`)

Extraction script counted 50 at BASE (matches the site's 50) and 61 at TARGET. All names are
`Microsoft.Xna.Framework.Content.<Name>`; file:line is the registration.

| Group | Readers | Count |
|---|---|---:|
| Primitives | Boolean, Byte, SByte, Int16, UInt16, Int32, UInt32, Int64, UInt64, Single, Double, Char, String (`PrimitiveContentTypeReaders.cpp:15-39`) | 13 |
| Math | Vector2, Vector3, Vector4, Matrix, Quaternion, Color, Plane, Point, Rectangle, BoundingBox, BoundingSphere, BoundingFrustum, Ray (`MathContentTypeReaders.cpp:13-39`) | 13 |
| Other value types | TimeSpan, DateTime, **Decimal (only if `SHARP_RUNTIME_HAS_NATIVE_INT128`)** (`DecimalDateTimeContentTypeReaders.cpp:12-18`) | 3 |
| Curve | CurveReader (`CurveContentTypeReader.cpp:10`) | 1 |
| Textures | TextureReader (legacy alias, **new**), Texture2DReader, Texture3DReader, TextureCubeReader (`Texture2DContentTypeReader.cpp:174,177`, `Texture3D...:67`, `TextureCube...:111`) | 4 |
| Font/audio/video | SpriteFontReader, SoundEffectReader, SongReader, VideoReader (`...:58`, `...:76`, `...:114`, `VideoContentTypeReader.cpp:117`, unconditional at TARGET) | 4 |
| Stock effects | BasicEffectReader, AlphaTestEffectReader, DualTextureEffectReader, EnvironmentMapEffectReader, SkinnedEffectReader (`StockEffectContentTypeReaders.cpp:156-168`) | 5 |
| General effect | EffectReader (D3D9 Effect Framework bytecode; renderer must report `CompiledEffects`) (`EffectContentTypeReader.cpp:63`) | 1 |
| Model family | VertexDeclarationReader, VertexBufferReader, IndexBufferReader, ModelReader (`ModelContentTypeReaders.cpp:378-387`) | 4 |
| Effect materials (**new**) | EffectMaterialReader, ExternalReferenceReader (`EffectMaterialContentTypeReaders.cpp:155,161`) | 2 |
| Closed generics | `ListReader<String>` (new), `ListReader<Int32>` (new), `DictionaryReader<String,Int32>` (new), `DictionaryReader<String,String>` (new), `ArrayReader<Vector3>` (new), `ListReader<Matrix>` (new), `ListReader<Rectangle>`, `ListReader<Char>`, `ListReader<Vector3>`, `DictionaryReader<String,List<Vector3>>` (new), `DictionaryReader<String,Object>` (new) | 11 |
| **Total** | | **61** |

New at TARGET vs BASE (11): TextureReader, ListReader<String>, ListReader<Int32>, DictionaryReader<String,Int32>,
DictionaryReader<String,String>, ArrayReader<Vector3>, ListReader<Matrix>, DictionaryReader<String,List<Vector3>>,
EffectMaterialReader, ExternalReferenceReader, DictionaryReader<String,Object>. The `KnownUnsupported` hook registers
nothing now (`modules/content/src/Xna/KnownUnsupportedContentTypeReader.cpp:36-44`).

Reader-count wording for the site: "61 built-in type readers (60 on toolchains without a native 128-bit integer, which drops
`DecimalReader`); no longer FFmpeg-dependent." The registered `VideoReader` reads the metadata only; playback still needs
the FFmpeg backend (`XnbBuiltInReaders.cpp:29-31`; `modules/CMakeLists.txt:9-57`; `modules/media/src/Internal/VideoDecoderUnavailable.cpp`).

### Container, compression, limits

* Header: magic `XNB`, platform byte from 16 accepted values (`w x m i a d X W n u p M r P g l`), version 4 or 5, flags
  (0x80 LZX, 0x40 raw LZ4 block, both bits = refused), total length; length is cross-checked against actual bytes.
  `include/CNA/Internal/Xnb/XnbHeader.hpp:63-150`; `ContentManager.hpp:708-796`.
* LZX: port of FNA's decoder, `Xnb/LzxDecoder.cpp` (31 850 bytes; BASE 31 832, unchanged apart from comments). Intel E8
  preprocessing is still not finished, matching FNA (`LzxDecoder.cpp:654-659`). LZ4: in-tree decoder, no external library,
  bounds-checked (`Xnb/XnbDecompression.cpp:92-140`). LZ4 already existed at BASE.
* Limits (defaults): file 64 MiB, decompressed 256 MiB, string 1 MiB, type readers 4096, shared resources 1 000 000,
  collection elements 10 000 000, nesting depth 256 (`XnbReadLimits.hpp:20-38`). Files above `INT32_MAX` are refused (`ContentManager.hpp:714-718`).
* Shared resources: two-pass fixup, `ContentReader::ReadSharedResource` (`ContentReader.hpp:305`, `ReadAsset` runs
  `ReadSharedResources` at `:327-331`).
* Error behaviour: `ContentLoadException` (with inner cause) for unregistered readers
  (`Xna/ContentReader.cpp:266`), bad magic/platform/version/length/compression, decompression failure. **New at TARGET**: a loose-file
  reader that throws any `std::exception` is wrapped in `ContentLoadException` (`ContentManager.hpp:570-588`), and
  `OpenStream` failures are `ContentLoadException` naming the asset (`ContentManager.cpp:204-240`).

### Extensibility surface

| Mechanism | API | Notes |
|---|---|---|
| XNB reader | `ContentTypeReader<T>::Read(ContentReader&, std::optional<T>)` + `ContentTypeReaderManager::AddTypeCreator(canonicalName, factory)` | `ContentTypeReader.hpp`; `ContentTypeReaderManager.hpp:36-52`; `RemoveTypeCreatorEXT` added |
| Reflective XNB payloads | `ReflectiveTypeReaderBuilder<T>(name).Field(&T::a)...Register()`; `.RegisterShared()` for reference types; `.SharedResourceField()`; `.EnumField()`; `.Base()`, `.Custom()`, `.RegisterAbstract()` | `ReflectiveTypeReader.hpp:355-554` **(new)** |
| Enum reader | `EnumTypeReader<TEnum>` | `ReflectiveTypeReader.hpp:289` **(new)**; not part of the 61 |
| Loose file | `LooseFileContentTypeReader<T>`: `GetExtensions()`, `T Read(const std::string& path, ContentManager&)`; register with `content.RegisterTypeReader<T>(std::make_unique<...>())` (per `ContentManager` instance, replaces an existing reader) | `LooseFileContentTypeReader.hpp:19-60`; `ContentManager.hpp:298-303` |
| Named CNJ loaders | `RegisterCnjLoader<T>(typeName, fn(json, cm))`, throws if `T` already has a reader or the pair repeats | `ContentManager.hpp:342-384` |
| CNB custom type | `RegisterCnbLoaderEXT<T>` | `ContentManager.hpp:440-458` |
| Stream source | protected virtual `OpenStream(assetName)`, protected `ReadAsset<T>(name, recordDisposable)`, protected `Dispose(bool)` | `ContentManager.hpp:171,188,208` **(new)** |

### ContentManager: what changed between BASE and TARGET (public/protected surface and behaviour)

`[impl]` `diff BASE ContentManager.hpp TARGET`, then source read.

* New protected seams: `Dispose(bool)`, `OpenStream`, `ReadAsset<T>`; `friend ContentReader` internals for typed external references.
* `Load<T>`: the debug "Loading asset" log moved after the cache lookup; `.cnb` tiers added; `TryReadAssetBytes` used for
  the `.xnb` tier so platform-packaged assets (Android) are served (`ContentManager.cpp:554-604`); the `.cnb` tiers use
  `std::filesystem::exists` plus `ifstream` and therefore **not** the packaged-asset route (see Open questions).
* `Load<Audio::SoundEffect>` is an explicit specialisation that never caches (move-only type) (`ContentManager.hpp:861-862`).
* Weak texture cache (`textureCache_`, `WeakTextureEntry`) **removed** (commit `975156d14`); loaded assets are held by
  `loadedAssets_` keyed by (type_index, lowercase-normalised name) until `Unload()`.
* Default root: `ContentManager(IServiceProvider*)` now leaves `RootDirectory` **empty** (XNA-faithful); `ContentManager()` and
  `Game::Content` use `"Content"` (`ContentManager.cpp:103-119`; `BASE: ContentManager.hpp:50` `= "Content"` for all ctors).
* Asset name resolution: root joined to name with `\` normalised to `/`; existing path resolved **case-insensitively** by
  walking directories (`ContentManager.cpp:504-548`); Android relative paths go to the packaged-asset namespace.
* `Unload()` = `loadedAssets_.clear()` (`ContentManager.cpp:244-247`); `Dispose(true)` calls it; assets are value types
  whose GPU state is shared-owned, so a copy you hold stays valid.
* Access: `Game` exposes `getContentProperty()` (returns `ContentManager&`); there is no `Content` member or pointer
  (`modules/runtime/include/.../Game.hpp:91-103`). `Load<T>` returns `T` **by value**.
* Loose extensions (`ContentManager.cpp`): Texture2D `.png .jpg .jpeg .bmp .gif .tga .tif .tiff .qoi` (754-756); TextureCube `.dds` (811-813);
  Texture3D `.cnj` (861-863); SoundEffect `.wav` (920-922); Effect `.cnj` (1049-1051); SpriteFont `.cnj` (1479-1481);
  AnimationClipEXT `.cnj` (1944-1946); Curve `.cnj` (1972-1974); Model `.cnj .gltf .glb` (4300-4306); skinned model
  `.skinnedmodel.json` (5875-5877); Song `.mp3 .ogg .wav .flac .opus .aac .wma` (6046-6048); Video `.mp4 .ogv .webm .mkv .avi .mov` (6062-6064).
  Registered `T`s: `Texture2D`, `TextureCube`, `shared_ptr<Texture3D>`, `SoundEffect`, `shared_ptr<Effect>`, `SpriteFont`, `Model`,
  `AnimationClipEXT`, `Curve`, `shared_ptr<SkinnedModelEXT>`, `Song`, `Video` (`ContentManager.cpp:6303-6316`). **`ShaderEffect` and `SoundBank`
  are not registered types.**

---

## Models/glTF

Runtime path `Load<Model>("name")`, where `name.gltf`/`name.glb` exists and no higher tier does.

| Ledger limit (BASE-era claim) | TARGET truth | Evidence |
|---|---|---|
| "first mesh group only" | **False.** `CollectMeshGroups` groups by skin plus one static group; every group is imported into one `Model`; `Model::SkinsEXT` carries each skin; `Tag` keeps the first skin for compatibility. (The doc comment above `ReadGltfModel` still says "only the file's FIRST mesh group": stale text; the code below it loops all groups.) | `ContentManager.cpp:2835-2838` (stale comment), `:2955` (`CollectMeshGroups`), `:3069`, `:3114`, `:3313`, `:4201` (loops over every group), `:4212` (`SkinsEXT`) |
| "unit scale 1.0" | **True.** Literal `1.0f` passed to `BuildSkeleton`, `ExtractMesh`, `ExtractSceneNodeClips`, `ExtractCamerasEXT`. Only `cna_tool_gltf_to_cnj [unitScale]` and `cna_tool_gltf_to_cnb --unit-scale` scale. No unit-scale key in `cna-content`. | `ContentManager.cpp:3084,3221,3569,4011,4252`; `tools/gltf_to_cnb/gltf_to_cnb.cpp:92-95` |
| "rigid node animation dropped" | **False for unskinned models**: retained as `ModelAnimationsEXT` (`ClipTargetSpaceEXT::SceneNode`). **True in one case**: a file with skins where extra rigid tracks are not carried by any skin; dropped with warning (`GLTF-295`) and a report diagnostic. | `ContentManager.cpp:3184-3246` (drop at `:3202-3211`, retained branch `:3213-3246`) |
| "factor-only PBR loss" | **False.** `usePbr = (material == null) \|\| !material->unlit`; factors read for any metallic-roughness material; vertex-coloured primitives keep PBR (strides 60 rigid / 80 skinned); `KHR_materials_pbrSpecularGlossiness` converted. | `GltfImportCore.cpp:2905-2965` |
| "`extensionsRequired` unchecked" | **False.** Refused by name unless the 21-record registry claims it; `extensionsUsed` unknown entries warn; `EXT_meshopt_compression` refused outright; Draco claimed only when `CNA_DRACO_AVAILABLE`. | `GltfImportCore.cpp:4583-4700,5150-5200` |
| Other topology | all seven primitive modes handled (strip/fan/loop converted; Draco allows only TRIANGLES/TRIANGLE_STRIP) | `docs/gltf-limitations.md` §2,§5 `[md]`; code `GltfImportCore.cpp:2709+` |

Extension registry (`GltfExtensionRegistryEXT`, `GltfImportCore.cpp:4583-4680`): 21 records. Claimed (accepted when required):
`KHR_texture_transform`, `KHR_mesh_quantization`, `KHR_materials_emissive_strength`, `KHR_lights_punctual` (approximated as up to 3
directional lights), `KHR_draco_mesh_compression` (build-dependent), `KHR_materials_unlit`, `KHR_materials_variants`,
`KHR_materials_ior`. Not claimed (refused when required): `KHR_materials_transmission` (approximated), `KHR_texture_basisu`,
`EXT_texture_webp`, `KHR_materials_pbrSpecularGlossiness` (converted), `KHR_materials_specular` (implemented with named limit),
`KHR_materials_clearcoat`, `KHR_materials_sheen`, `KHR_materials_volume` (all `ParsedButIgnored` for stock effects),
`EXT_meshopt_compression`, `EXT_mesh_gpu_instancing`, `KHR_materials_iridescence`, `KHR_materials_anisotropy`,
`KHR_materials_dispersion` (`NotDesired`). Full per-row text: `docs/gltf-limitations.md` §1 `[md]`, generated from and
checked against this registry by test `GltfLimitationsDoc.ExtensionTableAgreesWithTheRegistry` (`[test]` existence).

Changes glTF-importer BASE to TARGET (small): legacy `_TANGENT`/`_BINORMAL` VEC3 attributes imported as tangent VEC4
(`GLTF-480`, `GltfImportCore.cpp:2800-2862,3728-3778`); clearcoat/sheen/transmission/volume/iridescence **factor values now copied** into
`MaterialOut` (`MOD-2076`, `GltfImportCore.cpp:2977-3023`) for the CNAEXT `GltfMaterialBridge`/`ClusteredForwardEffect`
(`modules/graphics-ext/include/CNA/Graphics/GltfMaterialBridge.hpp`), while the registry still classifies those extensions
`ParsedButIgnored` for the stock effects; Unicode-safe external URIs; external-URI dependency listing for the build pipeline
(`CollectExternalUriDependenciesEXT`). cgltf version 1.15 (`third_party/cgltf/cgltf.h:4`).

Other Model facts:

* Model `.cnj` versions 1 and 2 (v2 adds `bones` and per-mesh `parentBone`); `cna_tool_gltf_to_cnj <in> <outDir> <baseName> [unitScale]`
  unchanged (`tools/gltf_to_cnj/gltf_to_cnj.cpp:1680`); `--dump-oracle` is a test-oracle mode. Sidecars resolve relative to the ContentManager root
  (unchanged; not re-read).
* Direct glTF and Model `.cnj` both fill `Model::getGltfImportReportEXTProperty()` (`ContentManager.cpp:4293,5176`).
* Skeletal animation (`SkinnedModelEXT`, `AnimationPlayer`, `AnimationClipEXT`), morph targets (`MorphTargetDataEXT`, header
  `MorphTargetEXT.hpp`), cameras (`ModelCameraEXT`), skins (`ModelSkinEXT`), variants exist as CNAEXT (`Model.hpp:219-303`). The site calls the
  morph type `MorphTargetEXT` in `docs/model-loading.html:372`; the type is `MorphTargetDataEXT` (header `MorphTargetEXT.hpp`).
* conformance: 296 `.gltf/.glb` fixtures under `tests/assets/gltf`, 62 files and 571 tests under `modules/content/tests/CNA/Internal/GltfImport` (counted).
  CNA's own summary of its campaign is `docs/gltf-campaign-retrospective.md` `[md]`.
* Model paths through `ContentManager` at TARGET: `.xnb`, `.cnb`, literal, `.cnj`, `.gltf`, `.glb`; through the pipeline: `.gltf/.glb/.cnj/.x/.fbx/.xnb -> .cnb`
  (and `.xnb` with the caveats above). There is no runtime FBX/`.x` importer; those are build-time only. `.cnamodel` (site) does not exist.
* Model schema 2 (CNB) preserves exact XNA vertex declarations, shared buffers and five stock effects for XNB-originated models
  (`Cnb/CnbModelV2Data.hpp`, `docs/cnb-format.md` §11.2 `[md]`).

---

## Corrections to existing site claims

Legend: the "TARGET truth" column is what the page should say; evidence is TARGET path:line. Line numbers for pages are raw HTML lines (checked with `grep -n`).

| Page (raw line) | Old claim | TARGET truth | Evidence |
|---|---|---|---|
| `docs/content-pipeline-xnb.html` header / callout (134), meta description (7,12,22), table (154), headings (124,211) | "CNA does not author XNB files"; "50 built-in readers (49 without FFmpeg)"; "XNB Content Pipeline" is read-side only | CNA reads **and writes** XNB; 61 readers (60 without native int128); VideoReader not FFmpeg-conditional | V1, V4; `XnbAssetWriter.hpp:49`; reader table |
| same (184-190) | "registry is empty by default; must call RegisterAllBuiltInXnbReaders() ... `#include <CNA/Internal/Xnb/XnbReaderRegistry.hpp>`" | A `Game` subclass registers automatically; standalone `ContentManager` still needs the call; header is `CNA/Internal/Xnb/XnbBuiltInReaders.hpp` | `Game.cpp:333-338`; `XnbBuiltInReaders.hpp:38` |
| same (284, known gaps) | "No ReflectiveReader"; "No EnumReader: enum-typed fields cannot be read"; "Collection readers implemented but unregistered" | `ReflectiveTypeReaderBuilder<T>` and `EnumTypeReader<TEnum>` exist; 11 closed collection readers are registered | `ReflectiveTypeReader.hpp:289,355-554`; reader table |
| same (~ "VideoReader follows FFmpeg availability") | "registered only on FFmpeg builds; 50 to 49" | registered unconditionally; playback needs backend | `XnbBuiltInReaders.cpp:29-31` |
| same (311) | "ResourceContentManager is a pure stub" | implemented (`OpenStream` over a `ResourceManager`); public `Load<T>` still uses the file ladder | `ResourceContentManager.cpp:12-77`; `ContentManager.hpp:509-517` |
| same (Testing section) | "112 C++ test sources with 978 definitions" (BASE) | 170 sources / 1872 in `modules/content/tests`, plus 47 / 487 in `modules/content-pipeline/tests` | V13 |
| same ("Prefers a .xnb ... falls back to loose files") | two tiers | `.xnb`, `.cnb`, then loose ladder | `ContentManager.hpp:494-568` |
| `docs/content-manager.html` (117) | "ResourceContentManager is a pure stub" | implemented | as above |
| same (121, 154, 164) | `T& Load<T>`; "manager returns a reference"; `RootDirectory` "std::string RootDirectory" property | `T Load<T>(const std::string&)` by value; property is `getRootDirectoryProperty()/setRootDirectoryProperty()` | `ContentManager.hpp:473`; `ContentManager.hpp:107` (`DEF_PROP`) |
| same (181, resolution-order list) | "Looks up the registered ContentTypeReader<T> ... Delegates to ReadAsset(fullPath)" | order is cache, `.xnb`, `.cnb`, literal `.cnb` name, `LooseFileContentTypeReader<T>` (literal path, `.cnj`, reader extensions) | `ContentManager.hpp:480-591` |
| same (307-334, 337, 389, custom reader sections) | `#include <CNA/Content/ContentTypeReader.hpp>`, `ContentTypeReader<T>::ReadAsset(path)` returning `unique_ptr`, `ContentManager::RegisterReader<T>(shared_ptr)`, "built-in readers ... cannot be overridden (throws std::runtime_error)", "registered readers are global" | Loose readers derive `LooseFileContentTypeReader<T>` (`T Read(path, ContentManager&)`), registered per instance with `RegisterTypeReader<T>(std::unique_ptr<...>)`; registering over a built-in type silently replaces it on that instance; `RegisterReader` does not exist; header is `Microsoft/Xna/Framework/Content/LooseFileContentTypeReader.hpp` | `LooseFileContentTypeReader.hpp:19-60`; `ContentManager.hpp:298-303` |
| same (341, callout) | "Custom types are loose-file only ... custom types cannot be loaded from an .xnb at all" | custom XNB readers via `ContentTypeReader<T>` + `AddTypeCreator`, or `ReflectiveTypeReaderBuilder<T>` | V7 |
| same (203, Texture2D row) | "Textures are cached by weak reference, so GPU memory is released once your last copy goes out of scope" | no weak texture cache at TARGET; `loadedAssets_` holds a copy until `Unload()` | `ContentManager.hpp:87` (no `textureCache_`); commit `975156d14` |
| same (160 vs 117, Unload) | "Disposes all cached assets" (row) vs "clears its internal maps without disposing" (status box) | `Unload()` only clears the cache map; held copies remain valid | `ContentManager.cpp:244-247` |
| same (251, Video row) | "There is no XNB VideoReader" | `VideoReader` is registered | `VideoContentTypeReader.cpp:117` |
| same (203, Texture2D row) | "Textures ... decoded via SDL3_image" | loose decode is `ImageLoader` (stb-based `STBI_rgb_alpha`) | `modules/graphics/src/Internal/ImageLoader.cpp:261,289,303` |
| `docs/model-loading.html` (116) | fixed order ".xnb, then a literal name, then name.cnj, then .cnj/.gltf/.glb" | `.xnb`, `.cnb` (new), literal `.cnb` name, literal path, `.cnj`, then `.cnj .gltf .glb` | `ContentManager.hpp:494-568` |
| same (143, 305) | "XNB registry is empty until you call ..."; "ContentManager resolves ... preferring an .xnb if one exists and otherwise reading the .cnj" | auto-registered in `Game`; add `.cnb` tier | V5, V3 |
| same (title/status; no pipeline mention) | model content path is "offline gltf_to_cnj" | also `cna-content build` and `cna_tool_gltf_to_cnb` produce `.cnb` (skeleton, animation, morph, lights kept; variants refused) | `cmake/Tool*.cmake`; `CnbModelFromCnj.cpp:491-499` |
| same (372) | type `MorphTargetEXT` | type `MorphTargetDataEXT` (header `MorphTargetEXT.hpp`) | `MorphTargetEXT.hpp:77` |
| `docs/3d-rendering.html` (771-788, 585-601) | "Load a `.cnamodel` asset"; `auto houseModel = content.Load<Model>(...)`; `houseModel->Draw`, `model->Meshes`, `model->Bones.Count()` | no `.cnamodel` format exists; `Model house = getContentProperty().Load<Model>("models/house"); house.Draw(...)`; `getMeshesProperty()`, `getBonesProperty().getCountProperty()` | `Model.hpp:219-225,401`; grep `cnamodel` in TARGET = none |
| `about.html` (103) | "A real .xnb content pipeline, with loose-file loading as a fallback" | now literally true in both directions: `cna-content` is a content pipeline that writes `.cnb`/`.xnb`; loading prefers `.xnb`, `.cnb`, then loose files. Reword to state what it produces | V1, V3 |
| `about.html` (151) | "Model tooling: runtime glTF plus the offline gltf_to_cnj converter" | add `cna-content`, `cna_tool_gltf_to_cnb`, `.x/.fbx` import at build time | V9; routes table |
| `features.html` (150-151) | "Content System & .xnb Pipeline ... A real read-side .xnb loader ... 50 ... CNA does not author XNB files"; "Extensible ContentManager with the ContentTypeReader<T> pattern" | 61 readers; writes XNB; loose readers are `LooseFileContentTypeReader<T>` | V1, V4; `LooseFileContentTypeReader.hpp` |
| `features.html` (153) | "VideoReader follows FFmpeg availability", "Closed generic readers still need explicit registration" | not FFmpeg-dependent; 11 closed generics preregistered; new ones still need registration | reader table |
| `features.html` (191) | compiled effects "on FNA3D and on opt-in EasyGL, SDL_GPU and Vulkan builds" | nine opt-in build options at TARGET (list in V14); defer to renderer fact sheet | `cmake/RendererSelection.cmake` |
| `features.html` (213) | "CNA's actual model content path is gltf_to_cnj" | one of several: direct runtime glTF, `.cnb`/`.xnb` from `cna-content`, `.cnj` from `gltf_to_cnj` | routes table |
| `architecture.html` (316, 327) | module tree lists `content/ audio/ ...`; `tools/` = "gltf_to_cnj, xna-oracle, reference dumpers" | add `content-pipeline/`; tools now include `content` (`cna-content`), `cnb_info`, `cnj_to_cnb`, `source_to_cnb`, `gltf_to_cnb`, `xnb` (conformance), `xna-pipeline-oracle` | `modules/CMakeLists.txt:352-355`; `ls tools` |
| `index.html` (202-204, card "Real .xnb Content Pipeline") | "read-side XNB loader ... it does not include an XNB authoring pipeline"; "Built-in readers must be registered explicitly at startup" | the project now includes an authoring pipeline (`cna-content`, CNB, XNB output); a `Game` registers built-ins itself | V1, V5 |
| `index.html` (209) | "An offline glTF 2.0 converter is CNA's actual content path for models" | see `features.html` row | routes table |
| `docs/faq.html` (160) | "CNA has no build-side content pipeline of its own and does not plan one" | it has one | V1 |
| `docs/faq.html` (343-347) | "Yes, for reading ... 50 ... CNA never writes an .xnb ... There is no ContentImporter, ContentProcessor or ContentCompiler ... 'XNB loader' is the accurate phrase; 'content pipeline' is not" | writes XNB; has Importer/Processor/Compiler in both native and XNA-shaped forms; call it "XNB loader **and** content pipeline" | V1; `modules/content-pipeline/include/.../Pipeline/` (107 headers) |
| `docs/verification.html` (365-372) | "Builds .xnb files with a design-time content pipeline / Reads .xnb and never writes one"; "50 (49...)"; "none registered until you make that call" | invert the "Builds .xnb" row (supported, with CNA-reported verification); 61 readers; auto-registered by `Game` | V1, V4, V5 |
| `docs/xna-compatibility.html` (182, 232, 235, 239, 244, 415, 428) | "CNA only ever reads them ... has no ContentImporter/ContentProcessor/ContentCompiler ... explicitly out of scope and will not be built"; "XNB is read-side only"; 50 readers | same correction; `Microsoft::Xna::Framework::Content::Pipeline` is implemented (128/128 types per generated report) | `[gen]` parity report; implementation files |
| `docs/migration-from-monogame.html` (118, 377-381, 410, 444) | 50/49 readers; "You must call RegisterAll..."; "Models: .fbx/.obj compiled to .xnb" row for CNA = XNB readers, glTF, gltf_to_cnj | `.fbx` and `.x` can now be built with `cna-content` to `.xnb`/`.cnb`; `.obj` is not a route; `.spritefont` + MGCB flow has a CNA equivalent (`.spritefont` via FreeType) | routes table; `XnaModelSourceContentPipeline.cpp:157,187` |
| `docs/roadmap.html` (152, 186) and `roadmap.html` (135, 217) | "XNB writing are not provided/absent", "ReflectiveReader for custom XNB types: Not started", 50/49 | XNB writing shipped; `ReflectiveTypeReaderBuilder` shipped (declared-field model, still no runtime reflection) | V1, V7 |
| `contribute.html` (229, 235) | "XNB reader gaps: 50/49"; "ResourceContentManager is the repository's only pure stub"; "`Unload()` clears its maps without disposing" | 61; RCM implemented; `Unload()` behaviour unchanged | V4, V6 |
| `docs/vs-alternatives.html` (104, 187-188, 279) | "Read-side loader 50 built-ins ... explicit startup"; "XNB content pipeline: Yes (via MGCB)" comparison | CNA also builds content itself; CNA is not a MonoGame pipeline replacement for MGCB workflows (no `.mgcb`) | V1 |
| `docs/tutorials/01-introduction.html` (113) | "CNA is an XNB loader, not an authoring pipeline" | correct to "loader and content pipeline" | V1 |
| `docs/tutorials/45-content-manager.html` (105, 110, 155, 161-186) | "no ContentImporter, no ContentProcessor and no ContentCompiler, so nothing here builds .xnb files"; "readers not registered automatically ... fresh ContentManager cannot read any .xnb"; "no ReflectiveReader"; "Default is empty string" | Pipeline exists; `Game` auto-registers; reflective builder exists; default root: `ContentManager(IServiceProvider*)` empty, `ContentManager()` and `Game::Content` "Content" | V1, V5, V7; `ContentManager.cpp:103-119` |
| `docs/tutorials/46-content-reader.html` (104) | "Custom types cannot be read from .xnb at all, because CNA has no ReflectiveReader" | can, via `ContentTypeReader<T>` + `AddTypeCreator` or `ReflectiveTypeReaderBuilder` | V7 |
| `docs/tutorials/83-migrate-monogame.html` (158-170) and `84-migrate-xna.html` (170-176) | "read-side ... no ContentCompiler, ContentImporter or ContentProcessor and never will"; 50/49; "readers are not auto-registered" | same corrections | V1, V4, V5 |
| `docs/tutorials/95-speedy-blupi.html` (135) | "50 ... (49 without video). Call RegisterAll... once at startup" | 61; `Game` registers | V4, V5 |
| `docs/tutorials/110-gltf-models.html` (108, 121-127 table) | 4-row candidate order without `.cnb`; "`Model* house = Content->Load<Model>(...)`" | add `.cnb` after `.xnb`; by value | `ContentManager.hpp:494-568` |
| `docs/tutorials/111-cnj-pipeline.html` (101, 113, formats table) | "CNJ ... not a compiled binary container and not a content pipeline"; ".xnb ... will never write it - there is no ContentImporter or ContentProcessor anywhere in the project"; formats table has no `.cnb` | CNB is the compiled container; `.cnj` is an input to `cna_tool_cnj_to_cnb`/`cna-content`; XNB is writable | V1, V2; `tools/cnj_to_cnb` |
| `docs/tutorials/35-model-loading.html` (116, 121, 268) | "does not run the XNA Content Pipeline"; ".xnb ... Produced by the original XNA Content Pipeline"; order `.xnb, .cnj, .gltf/.glb` | CNA has its own pipeline that can also build XNA `.x/.fbx`; `.xnb` may also come from CNA; `.cnb` tier; runtime FBX/`.x` importer still absent | V1, V3 |
| `docs/tutorials/22-blend-modes.html` (111, 153) | "Textures loaded via ContentManager are pre-multiplied by default" and "CNA's ContentManager::Load<Texture2D> pre-multiplies alpha at load time" | loose PNG/JPG decode is straight alpha (no premultiply in the loader); only `cna-content`'s `TextureProcessor` (default `premultiplyAlpha=true`) produces premultiplied `.cnb`/`.xnb`. The page contradicts itself | `ImageLoader.cpp:261-303`; `Texture2DContentPipeline.cpp:1104` |
| `docs/tutorials/45-content-manager.html` (155, Video row) and `docs/video-playback.html` | "Video ... Linux and macOS only ... compiles and then fails to link on Windows, Emscripten, Android" | Video/VideoPlayer types now always link; playback reports `NotSupportedException` without the FFmpeg backend (renderer/media agent to confirm wording) | `modules/CMakeLists.txt:9-57`; `modules/media/src/Internal/VideoDecoderUnavailable.cpp` |
| `docs/tutorials/121-video-playback.html` (139) | seven-argument `Video` ctor "for the XNB path" | still true; also used by CNB Song/Video loaders (`BuildVideoFromCnbEXT`) | `ContentManager.cpp:6287-6298` |
| `docs/shader-effects.html` (142, 199) and `docs/tutorials/24,52,58` | "CNA's content pipeline has a real Effect reader that consumes a `.cnj`" (loader wording) | fine as loader wording, but "content pipeline" is now a defined product; suggest "ContentManager's Effect reader" | terminology |

Search/nav: `search-index.json`, `sitemap.xml`, `documentation.html` (77-83), `tutorials.html` must gain entries when pages are added.

---

## Tutorial API mismatches

Checked every code fragment that calls `ContentManager`, `Load<T>`, readers or `Model` against TARGET headers
(`ContentManager.hpp`, `LooseFileContentTypeReader.hpp`, `Model.hpp`, `AnimationPlayer.hpp:33`). Correct form: from a `Game`,
`getContentProperty().Load<T>("name")`; `Load<T>` returns `T` by value (`std::any_cast<T>` of the cached copy,
`ContentManager.hpp:473-487`); root via `getContentProperty().setRootDirectoryProperty("Content")`; reader base is
`LooseFileContentTypeReader<T>`.

| Tutorial / page (raw line) | Quote | Correct API / problem |
|---|---|---|
| `docs/tutorials/110-gltf-models.html:108` | `Model* house = Content->Load<Model>("models/house");` and `house->Draw(world, view, projection);` | `Model house = getContentProperty().Load<Model>("models/house"); house.Draw(world, view, projection);` (no `Content` member, `Load` returns by value) |
| `docs/tutorials/110-gltf-models.html:93` (learn list) | "with one Content.Load<Model>() call" | `getContentProperty().Load<Model>()` |
| `docs/tutorials/111-cnj-pipeline.html:332` | `Model* hero = Content->Load<Model>("hero"); hero->Draw(...)` | by value, `getContentProperty()` |
| `docs/tutorials/111-cnj-pipeline.html:341` | `AnimationClip walk = Content->Load<AnimationClip>("hero_Walk");` | `Graphics::AnimationClip` is a `CNAEXT using` alias of `AnimationClipEXT` (`AnimationPlayer.hpp:33`) so the type is valid, but `Content->` is not; use `getContentProperty().Load<AnimationClipEXT>("hero_Walk")` |
| `docs/tutorials/45-content-manager.html:179` | `auto* tex = content.Load<Texture2D>("textures/terrain");` | `Load` returns `Texture2D` by value; `auto* tex` does not compile. Use `Texture2D tex = content.Load<Texture2D>(...)` |
| `docs/tutorials/45-content-manager.html:186` | `auto* sfx = content.Load<SoundEffect>("audio/explosion"); sfx->Play(0.8f, 0.0f, 0.0f);` | `SoundEffect` is returned by value (move-only, never cached, `ContentManager.hpp:861-862`): `auto sfx = ...; sfx.Play(...)` |
| `docs/tutorials/45-content-manager.html:165` | `ContentManager levelContent(&getServicesProperty(), "Content/Level1");` | valid (`ContentManager(IServiceProvider*, const std::string&)`, `ContentManager.hpp:144`) |
| `docs/tutorials/45-content-manager.html:161` | "Default is empty string (alongside the executable)" | accurate only for `ContentManager(IServiceProvider*)`; `ContentManager()` and `Game::Content` use `"Content"` (`ContentManager.cpp:103-119`) |
| `docs/tutorials/121-video-playback.html:131` | `Media::Video intro = Content.Load<Media::Video>("videos/intro");` | `Content.` is not a member; `getContentProperty().Load<Media::Video>(...)` |
| `docs/video-playback.html:147,336` | `auto video = content.Load<Video>("videos/intro");` | fine only if a local `ContentManager& content` exists; otherwise `getContentProperty()` |
| `docs/content-manager.html:349-363,392` | `Texture2D& playerTex = Content.Load<Texture2D>(...)`, `SoundEffect&`, `Song&`, `Model&`, `TileMap& map = Content.Load<TileMap>("maps/world1.tilemap.json")` | by value (no `&`), `getContentProperty()`; `TileMap` example uses non-existent `RegisterReader<T>` |
| `docs/content-manager.html:307-334,389` | `class LevelDataReader : public ContentTypeReader<LevelData> { std::unique_ptr<LevelData> ReadAsset(const std::string& assetPath) override ...}`; `ContentManager::RegisterReader<LevelData>(std::make_shared<...>())` | replace with tutorial 46's `LooseFileContentTypeReader<LevelData>` and `content.RegisterTypeReader<LevelData>(std::make_unique<...>())` (`ContentManager.hpp:298`) |
| `docs/render-targets.html:441-442,484,500` | `auto blurHEffect = content->Load<ShaderEffect>("shaders/blur_horizontal");` | no reader is registered for `ShaderEffect`; registered type is `std::shared_ptr<Effect>` from a `.cnj` Effect descriptor (`ContentManager.cpp:6311`); `Load<ShaderEffect>` throws "No reader registered for type" (`ContentManager.hpp:551-556`). Use `Load<std::shared_ptr<Effect>>` then downcast (as `docs/shader-effects.html:69` does) |
| `docs/3d-rendering.html:585-601,774,788` | `auto houseModel = content.Load<Model>("models/house"); houseModel->Draw(...)`; `for (auto& mesh : model->Meshes)`; `model->Bones.Count()` | `Model house = ...; house.Draw(...)`; `model.getMeshesProperty()`; `model.getBonesProperty().getCountProperty()` (`Model.hpp:219,225`) |
| `docs/3d-rendering.html:615` | `auto skybox = content.Load<TextureCube>("textures/skybox");` | TextureCube loads `.dds` (or `.cnj`/`.cnb`), fine if `content` is a `ContentManager&` |
| `docs/game-loop.html:190,474,530` | `playerTex = Content.Load<Texture2D>(...)`, `Game.Content.Load<SpriteFont>(...)` | `getContentProperty().Load<...>` |
| `docs/spritebatch.html:342,372` | `Content.Load<Texture2D>("player")`, `Content.Load<SpriteFont>("fonts/Arial20")` | same; SpriteFont has no default constructor (tutorial 45/47 handle with `std::optional`) |
| `docs/migration-from-monogame.html:333,403,540` (and the `Content->setRootDirectoryProperty` snippets) | `Content->setRootDirectoryProperty("Content"); Content->Load<Texture2D>("player");` and C# side `Content.Load` | `getContentProperty().setRootDirectoryProperty(...)` / `.Load<...>`; there is no `Content` pointer |
| `docs/vs-alternatives.html:327,370` | `content.Load<T>("name") — identical signature` | signature returns `T` by value; requires `getContentProperty()` |
| `docs/tutorials/47-game-component.html:144` | `getGameProperty().getContentProperty().Load<SpriteFont>("fonts/debug")` | valid shape; `SpriteFont` needs `std::optional` holder (page already does this) |
| `docs/tutorials/46-content-reader.html` code | `LooseFileContentTypeReader<LevelData>`, `GetExtensions()`, `Read(path, ContentManager&)`, `RegisterTypeReader<LevelData>(std::make_unique<...>())`, `Load<LevelData>` | **Correct** against TARGET |
| `docs/tutorials/35-model-loading.html` code | `getContentProperty().setRootDirectoryProperty("Content")`, `Model model = getContentProperty().Load<Model>(...)`, `getMeshesProperty()`, `CopyAbsoluteBoneTransformsTo(std::vector<Matrix>&)`, `getSkinsEXTProperty()`, `getGltfImportReportEXTProperty()` | **Correct** (`Model.hpp:219-303,381,401`); only prose (see Corrections) is stale |
| `docs/tutorials/36,08,09,14,15,16,17,24,26,29,53-58,61,64,69,71,98` `getContentProperty().Load<...>` | single-line loads | **Correct** |
| `docs/tutorials/120-xact.html:122` | "There is no Content.Load<SoundBank>()" | correct; `SoundBank` is not a registered type |
| `docs/tutorials/77-async-loading.html:258` | "`ContentManager::Load<T>()` is not thread-safe" | consistent with `ContentManager` (plain `unordered_map`, no lock); `CnbLoaderRegistry` and `ContentTypeReaderManager` are process-wide and guarded separately |
| `docs/tutorials/129-c-api-first-program.html` | no content API used | nothing to check; C ABI content surface exists (`content.h`) if a C content tutorial is wanted |
| `docs/tutorials/112,113` | EXT identifiers used exist at TARGET | all `...EXT` identifiers found in tutorials 110-114/35/36/45/46 exist in TARGET headers, except the type name `MorphTargetEXT` (header name, not a type) |
| `docs/tutorials/48-timestep.html` | no content calls | n/a |

---

## Proposed new pages/tutorials with outlines

All commands and APIs below are verified from TARGET source; things I could not verify by reading are flagged.

### Page P1: "Content Pipeline" (`docs/content-pipeline.html`)

Replaces the negative framing of `content-pipeline-xnb.html`; keep that page as the XNB reader/interop reference.

1. What it is and is not: build-time tool, two outputs (CNB default, XNB), importer to processor to writer, CNB is an output not the pipeline. (`docs/content-pipeline.md:8-40` `[md]`, consistent with `tools/content/content.cpp:300-303`.)
2. Getting the tool: built with the project (`cna_content_tool`, executable `cna-content`); no option to enable; optional deps table (FreeType `.spritefont`, FFmpeg for `.mp3/.wma/.wmv`, zlib, zstd, Draco, external fxc). Do **not** paste a build command that was not run; say "build target `cna_content_tool`".
3. Quick start: directory layout `ContentSource/{Models/robot.gltf,Textures/wall.png,Fonts/ui.cnj,Sounds/explosion.wav}`; `cna-content build ContentSource -o Content`; output tree with `.cna-content-manifest.json`, `.cna-content.lock`; single asset `cna-content build ContentSource/Textures/wall.png -o Content/Textures/wall.cnb`; `cna-content clean Content`.
4. Source-to-output routes table (the table above), with "which need optional dependencies" column.
5. Options: `--format`, `--config`, `--workers`, `--explain`, `--quiet`, `--xna-compatible`, `--only-configured-assets`, `--font-directory`, `--build-configuration`.
6. Per-asset configuration `.cna-content.json` (root `format`/`version`/`outputFormat`/`sourceRoots`/`assets`; per asset `logicalName`/`importer`/`processor`/`writer`/`outputFormat`/`parameters`); texture parameters `colorKey`, `textureFormat`, `generateMipmaps`, `premultiplyAlpha` (default true), `resizeToPowerOfTwo`; `generateChildAssets` for multi-group glTF.
7. Incremental builds and determinism: content-hashed manifest v9, `SKIP`/`BUILD`, `--explain`, atomic publication, lock file.
8. CMake: `cna_add_content(TARGET ... SOURCE_DIR ... OUTPUT_DIR ... [WORKERS n] [FORMAT xnb ...])` plus `add_dependencies(MyGame MyGameContent)`; cross-compile needs `CONTENT_EXECUTABLE`.
9. Loading the result: `getContentProperty().Load<Model>("Models/robot")` etc.; tier order.
10. For XNA porters: `.contentproj` (`cna-content build MyGame.contentproj -o Content`), the XNA-shaped API, `docs/xna-content-pipeline-migration.md` for depth; parity numbers attributed to CNA's generated report.
11. Extending (experimental): `ContentPipelineRegistry`, `RunContentCompiler`, `CNA::ContentCompiler` CMake alias, the example file paths; state "source/toolchain compatibility, not a plugin ABI".
12. Limits: no Effect in CNB, no HLSL compiler, `.xml` XNB-only, no CNB compression switch, no pipeline C ABI.

### Page P2: "CNB format reference" (`docs/cnb-format.html`)

Sections: goals/non-goals; primitives and byte order; 64-byte header table; 48-byte TOC entry; chunk ids and flags; `CMET`/`XREF`; versioning
(container vs schema); asset type id table (1-11, reserved range, custom range via FNV-1a); schema versions per type; compression (Zstd only,
opt-in per chunk, library/C-ABI only, measured trade-off with the single-machine caveat); limits table; determinism; loading path and
`ContentManager` tier; extending (`RegisterCnbLoaderEXT`, `CnbAssetTypeIdFromName`, `CnbWriter`); inspecting with `cna_tool_cnb_info`; what is
not implemented (Effect schema, embedded media, block-compressed texture writers, mmap "measured and rejected", package format).

### Page P3: "XNB interoperability (writing XNB)" (`docs/xnb-interoperability.html`) or a new section on `content-pipeline-xnb.html`

Commands: `cna-content build ContentSource -o Content --format xnb --xnb-platform windows --xnb-version 5 --xnb-profile reach --xnb-compress lzx`;
platform table (XNA 4.0: windows, windowsphone, xbox360 refused by default; others extended); reader-name style; what types write; verification
labels (impl/cna-rt/spec/golden/xna40) and the contradiction noted in Open questions; what glTF-to-XNB drops.

### Tutorial T1: "Build content with the pipeline, end to end" (new number, e.g. 130)

1. Create `ContentSource/` with a PNG, a WAV and a `.glb`.
2. `cna-content build ContentSource -o Content --explain` (show BUILD lines), run again (SKIP), then `cna-content clean Content`.
3. Add `.cna-content.json` with `parameters: {"colorKey": {"type":"string","value":"255,0,255"}}` on one texture; rebuild and show only that asset rebuilds.
4. In `LoadContent()`: `getContentProperty().Load<Texture2D>("Textures/wall")`, `Load<Model>("Models/robot")`, `Load<SoundEffect>("Sounds/explosion")` (note the extensionless logical names).
5. Show the resolution tier: leave a same-named `.png` beside `wall.cnb`; the `.cnb` wins (`ContentManager.hpp:527-534`).
6. CMake: `cna_add_content(TARGET GameContent SOURCE_DIR ContentSource OUTPUT_DIR Content)` and `add_dependencies`.
7. Validate with `cna_tool_cnb_info Content/Models/robot.cnb` (`--refs` lists `Textures/...` dependencies).

### Tutorial T2: "Producing XNB from CNA" (XNA porters)

`--format xnb` builds, `--xnb-platform windows`, `--xnb-compress lzx`; loading back in CNA needs no registration inside a `Game`; how to load in XNA/MonoGame is
**not verified by me** (CNA's own harness is the only evidence: `tests/interop/xna40/`), so present as "CNA reports".

### Tutorial T3: "Custom content types end to end" (extends tutorial 46)

Two halves: (a) XNB: `ContentTypeReader<T>` + `ContentTypeReaderManager::AddTypeCreator` or `ReflectiveTypeReaderBuilder<T>("Ns.Type").Field(...).Register()`; (b) CNB: `CnbAssetTypeIdFromName("MyGame.Level")`,
`CnbWriter`, `RegisterCnbLoaderEXT<T>`; optional: a custom `cna-content` executable from `modules/content/examples/custom-content-compiler.cpp`
(`RegisterBuiltInContentPipeline`, `registry->RegisterImporter/Processor/Writer`, `RunContentCompiler`), flagged experimental.

### Tutorial T4: "Loading glTF three ways" (rewrite of 110/111 flow)

Direct runtime glTF; `cna-content build` to `.cnb`; `gltf_to_cnj` for unit scale (`cna_tool_gltf_to_cnb --unit-scale`). Table of what survives each route (cameras, material variants, import report,
multi-skin, rigid animation), from the sections above.

### Updates (not new pages)

Tutorials 35, 45, 46, 110, 111 and pages content-manager, model-loading, content-pipeline-xnb per the tables above; `docs/tutorials/22` premultiply statement; add `.cnb` to every "formats side by side" table.

---

## Open questions

1. **XNA 4.0 verification wording.** `docs/xnb-interoperability.md` (2026-09-03) says nothing has been run against a real XNA runtime; `tests/interop/xna40/README.md` (2026-09-06) and `cna-content` help text say the harness ran 6/6 uncompressed and 6/6 LZX under Wine. Likewise `docs/content-pipeline.md:467-470` says "not verified against a genuine fxc" while the parity report says it was measured with the June 2010 `fxc` through Wine. No committed machine-readable result log found in the tree; I could not run anything. Recommend the site say "CNA reports ..." with the date.
2. **`.cnb` on packaged-asset platforms (Android).** The `.xnb` tier uses `TryReadAssetBytes` (packaged assets, case-insensitive); the `.cnb` tiers use `std::filesystem::exists` and `CnbDocument::ParseFile` (`ifstream`). Whether `.cnb` loads from an APK is unverified.
3. **`ResourceContentManager` public route.** Base `Load<T>` uses the file ladder and never calls `OpenStream`; only derived classes can call protected `ReadAsset<T>`. Confirm the intended public usage before describing it as "loads embedded resources".
4. **Decimal reader.** `SHARP_RUNTIME_HAS_NATIVE_INT128` is defined by sharp-runtime (not in the worktrees). I could not confirm which supported toolchains define it, so "61 (60 without native int128)" is the safe wording.
5. **Tutorial 22 premultiply claim.** I found no premultiply in `ImageLoader.cpp`/`Texture2D(assetName, device)`; the statement appears false for loose images (and BASE). Owner of graphics content should confirm.
6. **CNB Model versus direct glTF parity.** Cameras, material variants, import report and multi-skin are only on the direct path by my reading. Confirm `SkinsEXT` behaviour for a multi-skin file built with `generateChildAssets` (separate models per skin).
7. **`.x/.fbx` to `.cnb`** is stated by the source comment and the generated report but I did not trace `ModelProcessor` output through `ModelContentWriter` for those inputs.
8. **Renderer scope surprise.** `docs/gltf-campaign-retrospective.md` records `OPEN[retired]`, `[retired]` and `[retired]` as "retired 2026-09-17", while the site says "50 renderer identities across 46 families". Not my domain; flag for the renderers fact sheet. Also the compiled-effects options grew from three to nine (V14).
9. **`graphics-ext` glTF consumption.** New CNAEXT `GltfMaterialBridge`/`ClusteredForwardEffect` consume clearcoat/sheen/volume/iridescence factors that the core registry still labels `ParsedButIgnored`; the site should not call those extensions "ignored" globally without qualifying the stock-effect scope.
10. **Stale text inside CNA docs** (do not copy): `docs/content-pipeline.md:1141-1143` says the pipeline has no `.contentproj`, contradicted by the CLI; manifest "version 8"; the comment above `ReadGltfModel` (`ContentManager.cpp:2835-2838`) still describes first-group-only, no-scale behaviour.
11. **Xbox 360 wording.** See the Xbox row above: code converts texture payloads, help text and docs say it does not. Do not describe
    Xbox output beyond "refused by default; an opt-in flag produces unverified candidate files".
12. **Performance and size numbers** (CNB compression ratios, mmap timings, scheduler speedups) are single-host developer measurements; whether to show them at all on the site is an editorial choice.
