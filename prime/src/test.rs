#[cfg(test)]
use crate::validation::{validate_deadline, validate_priority};

#[test]
fn deadline_validation_test_true() {
    let cases = vec![
        // Short Cases
        "20-w",
        "20-h",
        "20-m",
        "20-s",
        "20-d",
        "2-d",
        "200-w",
        // Long Cases
        "2011-09-01",
        "2011-10-31",
        "2011-10-30",
        "1875-10-04",
        "1911-11-05",
    ];

    for case in cases {
        match validate_deadline(case) {
            Ok(s) => assert!(s == "SHORT" || s == "LONG"),
            Err(_e) => assert!(false),
        }
    }
}
#[test]
fn deadline_validation_test_false() {
    let cases = vec![
        // Short Cases
        "20hs",
        "20ms",
        "20ww",
        "2ss",
        "2000w",
        // Long Cases
        "2011-13-10",
        "2011-10-40",
        "1765-10-10",
        "2019-04-31",
    ];
    for case in cases {
        match validate_deadline(case) {
            Ok(s) => assert!(!(s == "SHORT" || s == "LONG")),
            Err(_e) => assert!(true),
        }
    }
}

#[test]
fn priority() {
    assert!(validate_priority(0).unwrap() == 0);
    assert!(validate_priority(1).unwrap() == 1);
    assert!(validate_priority(2).unwrap() == 2);
    assert!(validate_priority(3).unwrap() == 3);
    assert!(validate_priority(4).is_err());
    assert!(validate_priority(100).is_err());
    assert!(validate_priority(5).is_err());
}
