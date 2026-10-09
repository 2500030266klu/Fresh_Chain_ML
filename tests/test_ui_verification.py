import urllib.request
import re

def test_no_engine_active_badge():
    for page in ["/", "/models", "/lifecycle", "/eda"]:
        req = urllib.request.urlopen(f"http://127.0.0.1:5000{page}")
        assert req.status == 200
        html = req.read().decode("utf-8")
        assert "Engine Active" not in html, f"Found 'Engine Active' on {page}!"
        assert "99.7% F1" not in html or page in ["/", "/models", "/lifecycle"], "Check F1 badge"
    print("[OK] Successfully verified 'Engine Active' is removed from navbar on all pages.")

def test_models_page():
    req = urllib.request.urlopen("http://127.0.0.1:5000/models")
    assert req.status == 200, f"Expected 200, got {req.status}"
    html = req.read().decode("utf-8")
    
    print("\n=== /models VERIFICATION ===")
    # 1. Check all 8 tabs
    tab_matches = re.findall(r'id="model-tab-btn-(\d+)"[^>]*data-target="model-panel-(\d+)"[^>]*data-model="([^"]+)"', html)
    print(f"Found {len(tab_matches)} tab buttons:")
    assert len(tab_matches) == 8, f"Expected 8 tabs, found {len(tab_matches)}"
    for btn_idx, panel_idx, model in tab_matches:
        print(f"  Tab #{btn_idx} -> Target: model-panel-{panel_idx} -> Model: {model}")
        assert btn_idx == panel_idx, f"Mismatch between button {btn_idx} and target {panel_idx}"
    
    # 2. Check all 8 panels
    panel_matches = re.findall(r'id="model-panel-(\d+)"[^>]*data-model="([^"]+)"', html)
    print(f"Found {len(panel_matches)} model panels:")
    assert len(panel_matches) == 8, f"Expected 8 panels, found {len(panel_matches)}"
    
    # 3. Check Chart.js diagnostic canvases
    canvases = re.findall(r'id="diagChart-(\d+)"', html)
    print(f"Found {len(canvases)} diagnostic canvases: {canvases}")
    assert len(canvases) == 8, f"Expected 8 diagnostic canvases, found {len(canvases)}"
    
    # 4. Check confusion HUD
    tns = len(re.findall(r'True Negatives \(TN\)', html))
    fps = len(re.findall(r'False Positives \(FP\)', html))
    fns = len(re.findall(r'False Negatives \(FN\)', html))
    tps = len(re.findall(r'True Positives \(TP\)', html))
    assert tns == 8 and fps == 8 and fns == 8 and tps == 8, "Expected 8 of each HUD element"
    print("[OK] All 8 models verified in deep dive with interactive charts and confusion HUDs.")

def test_lifecycle_page():
    req = urllib.request.urlopen("http://127.0.0.1:5000/lifecycle")
    assert req.status == 200, f"Expected 200, got {req.status}"
    html = req.read().decode("utf-8")
    
    print("\n=== /lifecycle VERIFICATION ===")
    # Check H1 has 'Lifecycle'
    h1_matches = re.findall(r'<h1[^>]*>\s*Lifecycle\s*</h1>', html)
    assert len(h1_matches) > 0, "Lifecycle H1 title not found"
    print("[OK] Has <h1 ...>Lifecycle</h1>")
    
    # Check for forbidden strings
    m1_m6_matches = re.findall(r'm1-m6|M1-M6|\(m1-m6\)|m1 lifecycle', html, re.IGNORECASE)
    assert len(m1_m6_matches) == 0, f"Found forbidden m1-m6 text: {m1_m6_matches}"
    print("[OK] No 'm1-m6' or 'm1 lifecycle' references found")
    
    # Check for raw LaTeX formulas
    formula_matches = re.findall(r'\|y\s*-\s*Xw\||\$|\\lambda|\\Delta', html)
    assert len(formula_matches) == 0, f"Found forbidden LaTeX formulas: {formula_matches}"
    print("[OK] Zero raw LaTeX formulas on lifecycle page")
    
    # Check paired images in lifecycle
    images = re.findall(r'<img[^>]+src="([^"]+)"', html)
    print(f"Found {len(images)} images embedded on /lifecycle:")
    for img in images:
        print(f"  Embedded Image: {img}")
    assert len(images) >= 6, f"Expected at least 6 paired stage images, found {len(images)}"
    
    # Check zoom buttons
    zoom_targets = re.findall(r'data-img="([^"]+)"', html)
    print(f"Found {len(zoom_targets)} zoomable plot targets on /lifecycle:")
    for z in zoom_targets:
        print(f"  Zoom Target: {z}")
    assert len(zoom_targets) >= 6, f"Expected at least 6 zoom targets, found {len(zoom_targets)}"
    
    # Verify each zoom image actually loads via HTTP
    for z in zoom_targets:
        img_url = f"http://127.0.0.1:5000{z}"
        img_req = urllib.request.urlopen(img_url)
        assert img_req.status == 200, f"Failed to load image: {img_url}"
    print("[OK] All embedded stage images return HTTP 200 OK.")

if __name__ == "__main__":
    test_no_engine_active_badge()
    test_models_page()
    test_lifecycle_page()
    print("\n>>> ALL SYSTEM & USER VERIFICATION REQUIREMENTS PASSED! <<<")
