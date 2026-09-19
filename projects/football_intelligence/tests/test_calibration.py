from projects.football_intelligence.src.core.calibration import calibration_bins, expected_calibration_error

def test_calibration():
    rows=[{"predicted_probability":0.9,"won":True},{"predicted_probability":0.1,"won":False}]
    assert len(calibration_bins(rows))==2
    assert expected_calibration_error(rows)==0
