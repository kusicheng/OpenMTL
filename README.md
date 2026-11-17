# OpenMTL
The front end and user-facing application for BackToMTL, an accessible, fast, and lightweight option for complex, mass translation

## Repository boundaries

OpenMTL owns the frontend and user-facing application. [BackToMTL](https://github.com/kusicheng/backtomtl) owns the translation backend, image processing, OCR, detection, rendering, and related training code. [RagMTL](https://github.com/kusicheng/ragmtl) owns MAGRA retrieval and benchmarking.

These are separate repositories. Keep implementation in its owning repository; share functionality through explicit imports, supported APIs, or a deliberately abstracted shared component.
