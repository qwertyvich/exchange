# Casper Exchange — mascot assets

Reference: the user's supplied `2026-11-03 14.39.58.jpg`, a friendly white ghost with blue highlights. Prepared using the built-in **imagegen** tool in transparent image editing mode. No CLI/API generation was used.

- `ghost-source.png`: original transparent tool output, retained without modification.
- `../../frontend/public/brand/casper-ghost.webp`: production asset, 384×384, alpha preserved. Mechanically resized and WebP encoded at quality 0.92 using Chromium canvas; no additional drawing or generative changes.
- `../../frontend/public/brand/casper-sunglasses.svg` and `casper-suitcase.svg`: separate code-native accessories on the same 100×100 coordinate system, so they can remain stationary while the body moves. The suitcase is in the character's anatomical right hand, on the viewer's left.
- `../../frontend/public/brand/casper-favicon.svg`: lightweight code-native tab icon.

Exact prompt sent to the built-in tool:

> Use case: background-extraction / identity-preserve. This is an edit of the supplied ghost image, which is the edit target. Prepare a clean, production-ready transparent PNG mascot asset for Casper Exchange. Preserve the EXACT same friendly white ghost silhouette, round dome, small flipper arms, dark navy outline, black oval eyes, smiling mouth, pale sky blue cheek ovals, sky blue bottom edge and top-right blue highlight. Remove only the black background and the subtle JPEG texture/noise. The ghost must be opaque white inside, with a genuinely transparent outside, no fake checkerboard, no black matte or black halo, no ground, no shadow outside the contour, no text, no logo. Keep the whole character visible. Center the ghost in a square canvas with only about 6 percent transparent padding on each side, so its silhouette occupies roughly 88 percent of the square height and width. Do NOT add sunglasses, luggage or accessories: these will be separate animated code layers. No redesign of the face, no new pose, no extra limbs. Clean smooth dark contour and soft blue highlights, same illustration style as the reference.

Final targeted cleanup prompt, using the first output as its edit target:

> Precise cleanup edit of this transparent Casper ghost asset. Preserve the current exact canvas dimensions, position, outline, silhouette, face, blue highlights, cheek circles and blue bottom border. Make ONE targeted correction only: remove the dirty grey speckled circular patch from the lower central white belly. That entire white body area must be smooth clean opaque white, seamlessly matching the surrounding white body. No grey stain, no transparency hole, no new shadows, no noise or artifacts. Do not redraw or reposition the eyes, arms, mouth, contour or any blue details. Keep outside transparency. No sunglasses, no luggage, no text.
