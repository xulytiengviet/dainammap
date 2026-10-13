# Đại Nam Map — 1838 ↔ 2025

Dự án WebGIS so sánh ảnh lịch sử Đại Nam (ảnh ghi **1838**, niên đại cần kiểm chứng) với bản đồ Việt Nam 2025.

Bộ phát hành đầy đủ được tạo trong cuộc trò chuyện ChatGPT ngày 13/10/2026: `dainammap-webgis.zip`, gồm `index.html`, ảnh gốc PNG, PMTiles v3 raster, `tools/build_pmtiles.py`, giấy phép MIT và hướng dẫn.

**Quan trọng:** PMTiles được số hóa theo tọa độ điểm ảnh, **chưa nắn chỉnh địa lý**. Không thể khẳng định chồng khít ranh giới lịch sử lên hiện đại nếu thiếu GCP lịch sử có kiểm định.

## Cài GitHub Pages
Giải nén ZIP và tải **toàn bộ nội dung thư mục `dainammap/`**, kể cả `assets/`, vào gốc nhánh `main`. Mở Settings → Pages → Deploy from a branch → `main` → `/(root)`.

Mã ứng dụng MIT © 2026 Long Ngo; quyền với ảnh tư liệu cần xác minh riêng. Công nghệ: Leaflet, PMTiles, OSM. Tham khảo giao diện `xulytiengviet/maparchive`.
