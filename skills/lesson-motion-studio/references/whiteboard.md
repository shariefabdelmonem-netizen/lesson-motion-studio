# Colored hand-drawn whiteboard specification

## Art direction and palette

Use a clean warm cream canvas (#FAF7F0) and charcoal outlines (#263238).
Combine precise educational relationships with polished hand-drawn editorial illustrations.
Use two to four flat colors per scene in addition to outlines and background; do not use the whole palette at once.
Starting palette: petrol #247C74, muted sage #A7B8A0, sand #E7CC99, calm blue #789EB5, coral #D97662.
Adapt accents to the lesson rather than assigning the same subject colors everywhere.
Use color for a role or contrast and add labels or shapes so meaning never depends on color alone.
Avoid gloss, heavy gradients, deep shadows, neon colors, 3D characters and cinematic backgrounds unless explicitly requested.
Keep titles and important labels in Cairo; allow a meaningful word or label in an accent color with readable contrast.
Use light paper texture or hatching only when it remains unobtrusive at the final resolution.

## Illustrations, characters and continuity

Use finished illustrative forms with clear silhouettes, controlled internal details and consistent line weight.
Use expressive clothed characters when a person or action explains the lesson; do not add people to every diagram.
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
Draw outlines first and add flat color fills after the relevant outline is built; avoid colored silhouettes appearing before their boundary when claiming pen drawing.
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
Keep static interface headings distinct from animated teaching words; hold finished text for reading.

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
Check marks identify the right word, result or region and do not imply an answer too early.
Use pass, fail, not_checked, or not_applicable with a concrete reason and evidence in qa.json.
Do not claim finished visual or audio review from a storyboard, configuration or static-frame inspection alone.
