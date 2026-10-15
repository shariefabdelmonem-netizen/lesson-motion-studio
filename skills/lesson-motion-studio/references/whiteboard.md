# Colored hand-drawn whiteboard specification

## Art direction and palette

Use a clean warm cream canvas (#FAF7F0) and dark graphite-pencil outlines (#263238).
Combine precise educational relationships with polished hand-drawn editorial illustrations.
Use two to four colored-pencil hues per scene in addition to outlines and background; do not use the whole palette at once.
Starting palette: petrol #247C74, muted sage #A7B8A0, sand #E7CC99, calm blue #789EB5, coral #D97662.
Adapt accents to the lesson rather than assigning the same subject colors everywhere.
Use color for a role or contrast and add labels or shapes so meaning never depends on color alone.
Avoid gloss, heavy gradients, deep shadows, neon colors, 3D characters and cinematic backgrounds unless explicitly requested.
Keep titles and important labels in Cairo; allow a meaningful word or label in an accent color with readable contrast.
Build color with visible directional pencil strokes, modest pressure variation and small areas of paper showing through. Keep the texture legible without obscuring labels or exact diagrams at final resolution; avoid uniform digital fills and airbrush gradients.

## Illustrations, characters and continuity

Use finished illustrative forms with clear silhouettes, controlled internal details and consistent line weight.
Use slightly childlike expressive characters, rounded silhouettes and friendly faces when a person or action explains the lesson.
Scale the childlike treatment to the learner: more playful for primary learners, restrained and respectful for teenagers.
Avoid baby proportions, excessive cuteness, toy-like math symbols or a childish narrator tone for older students.
Keep characters away from exact diagrams while measurements, operators and relations are being explained.
Avoid stick figures as the default and avoid adding detail that obscures the teaching relation.
Design simple proportional faces with brows, eyes, nose and mouth; change expression or pose only for a relevant event.
Keep hands, clothing, hair and body proportions coherent; do not force hair, skin, dress or gender appearance from a country stereotype.
Reuse an approved character asset or model sheet for recurring identities instead of generating each scene independently.
Record recurring character traits, palette and asset paths in project.json.
Use consistent illustrated icons with the same outline weight, palette and level of detail.
Do not mix unrelated clipart styles or conceal asset defects through small display size.
If image generation is used, inspect actual assets and preserve alpha where required; deterministic paths still own exact mathematics, labels, maps and science relationships.

## Concrete examples and composition

Render the actual observable action promised by the script before moving to abstract representation.
Give every instructional point and every example in the narration a drawing that explains its specific action or relation at the time it is taught. Map each point and example to its drawing and timestamp in the storyboard; a written sentence or generic icon alone does not count. If the duration is too short, reduce the teaching scope while preserving a meaningful drawing for each retained point and example.
For a fence example, show a garden and fence boundary, trace the fence length, then simplify the same boundary into a measured rectangle.
For grammar, depict the relevant event, then build the sentence while keeping the target relation visible.
Use a focal illustration large enough to read, supporting details with clear hierarchy and generous whitespace.
Change composition when the teaching function changes rather than repeating the same centered drawing and bottom equation.
Preserve recurring objects through meaningful transformations instead of clearing the entire board on every beat.
Do not add icons or animation merely to satisfy a diversity quota.
Keep exact geometry and scales accurate: never jitter equal parts, measured lengths, map boundaries or vector directions for a handmade appearance.
Allow gentle controlled line irregularity only on illustrative outlines that do not encode a precise relation.

## Stroke drawing and typography

Create vector paths or separated ink layers and reveal each stroke from start to end at roughly constant arc length with eased endpoints.
Draw outlines first, then reveal colored-pencil shading through successive strokes inside the relevant form; avoid instant fills or colored silhouettes appearing before their boundary.
Place the pen tip at the revealed endpoint; lift or hide it when moving between disconnected paths.
Animate one drawing focus at a time; do not show multiple simultaneous pens for unrelated drawing and writing.
Keep the pen or hand outside text during reading holds and hide it when drawing stops.
For a hand cutout, use a generated or licensed asset and inspect fingers, grip, alpha and calibrated contact point.
A native drawn pen is acceptable when a good hand asset is unavailable.
Shape complete Arabic words with Cairo and RTL before tracing their ink paths.
Reveal actual shaped glyph strokes in reading direction and retain connected forms, dots and diacritics in the final text.
Use LTR for English and mathematical expressions where needed; explicitly compose mixed runs so numbers, units, operators and parentheses retain meaning.
Do not reverse an equation as a side effect of applying RTL to its enclosing sentence.
Preserve text correctness over simulated handwriting, but do not label a fade or rectangular wipe as pen writing.
Draw all visible headings and labels on first appearance, including interface-like scene labels; hold finished text for reading.
Reuse previously drawn elements without requiring repeated drawing on every frame or scene.

## Explanatory marks and motion

Draw a circle around the intended completed target, not a nearby number or word.
Use arrows with meaningful start and end points; do not cross unrelated text.
Place translucent highlights behind readable ink; schedule them after writing when that improves clarity.
Keep every answer hint absent during the actual thinking interval, including colored circles and labels.
Use subtle head, arm or facial motion only for the event being explained; avoid idle mouth animation or constant decorative movement.
Use simple camera moves only when they clarify scale, location or focus; pause movement while a learner reads.
Prefer logical carryover and transformations between scenes to loud bounces or arbitrary transitions.

## Review gates

Inspect exported frames during drawing, writing, coloring, transition, reading hold, question and answer.
Check pen contact, absence of competing pens, readable Cairo, correct mixed directions, consistent characters and exact educational relations.
Check that the concrete example is visible, each asset supports the learning objective and the abstract diagram preserves its relationship.
Compare the exported video against the full script: for each explanatory point and example, record the matching drawing, its timestamp and a frame showing how it conveys the meaning. Fail the visual coverage check for any missing or merely decorative drawing.
Check marks identify the right word, result or region and do not imply an answer too early.
Use pass, fail, not_checked, or not_applicable with a concrete reason and evidence in qa.json.
Do not claim finished visual or audio review from a storyboard, configuration or static-frame inspection alone.

## Storytelling and unbranded delivery

Build a compact educational story rather than an unrelated illustrated introduction followed by a lecture.
Use a familiar situation, one clear challenge, an observable discovery and a resolution that depends on the target concept.
Carry the same character, object and setting into the explanation and application where useful.
Example for perimeter: a pupil plans a fence for a school garden, first notices four sides, measures them, adds the lengths and obtains the required fence length.
Keep the mathematical boundary on a consistent scale and separate perimeter from planted area.
Use a new near-transfer challenge for the final quiz and retain the real silent thinking interval.
Do not add drama, extra characters or conversations that crowd out the learning objective.
Use one narrator unless the user explicitly asks for additional voices.
Record which story event motivates each teaching step and verify this link in exported frames.
Do not show or narrate the user's name, signature, job title or logo by default.
Remove inherited template credits and end cards when reusing an older project.
Only add branding when explicitly requested for the current output; inspect the actual beginning, ending and captions for accidental carryover.

## All-element stroke coverage gate

Every visible semantic element must have a real stroke-drawing sequence on its first appearance: characters, faces, clothing, plants, fences, icons, exact diagrams, titles, labels, numbers, equations and explanatory marks.
Do not exempt supporting illustrations or introduce completed characters beside an animated main diagram.
Keep a per-element manifest with ink paths, reveal ordering, start/end times, outline completion, color-fill timing and exported review evidence.
Trace ink paths with a single pen endpoint and lift it between disconnected paths. Reveal colored-pencil strokes only after the corresponding outline.
A slide-in, fade-in, scale-up or rectangular wipe never satisfies this gate.
A clean background may stay static. A finished element may hold, move or carry over once its first drawing has been shown.
Use a wide tracked marker path for highlights instead of instant colored boxes.
Inspect start, mid-stroke and completion frames for each element; do not infer complete coverage from the main diagram.
Fail all_elements_hand_drawn when any new element appears completed without drawing; use not_checked when evidence is absent.
Reduce detail or element count to fit the lesson duration instead of skipping the stroke sequence.
Do not claim complete hand-drawn coverage before every manifest entry passes.
