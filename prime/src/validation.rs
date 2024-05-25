use crate::task::getroot;
use std::io::{Error, ErrorKind};
use std::path::Path;
use std::process;

use regex::Regex;
pub fn validate_deadline(deadline: &str) -> Result<&str, Error> {
    let dl_re = match Regex::new(r"^\d{1,3}[\-][wdhms]$") {
        Ok(r) => r,
        Err(e) => {
            eprintln!("{}", e);
            process::exit(1);
        }
    };
    let date_re = match Regex::new(
        r"^((18|19|20)[0-9]{2}[\-.](0[13578]|1[02])[\-.](0[1-9]|[12][0-9]|3[01]))|(18|19|20)[0-9]{2}[\-.](0[469]|11)[\-.](0[1-9]|[12][0-9]|30)|(18|19|20)[0-9]{2}[\-.](02)[\-.](0[1-9]|1[0-9]|2[0-8])|(((18|19|20)(04|08|[2468][048]|[13579][26]))|2000)[\-.](02)[\-.]29$",
    ) {
        Ok(r) => r,
        Err(e) => {
            eprintln!("{}", e);
            process::exit(1);
        }
    };
    if dl_re.is_match(deadline) {
        Ok("SHORT")
    } else if date_re.is_match(deadline) {
        Ok("LONG")
    } else {
        Err(Error::new(
            ErrorKind::Other,
            "Please provide a proper deadline (--help for more details)",
        ))
    }
}

pub fn validate_priority(priority: u8) -> Result<u8, Error> {
    if priority < 4 {
        Ok(priority)
    } else {
        Err(Error::new(
            ErrorKind::Other,
            "Priority must be greater than equal to 0 and less than 4!",
        ))
    }
}

pub fn has_spl_chars(query: &str) -> bool {
    let splcheck = Regex::new(r"[\[!@#$%^&*(),.?\]+]").unwrap();
    if splcheck.is_match(query) {
        true
    } else {
        false
    }
}

pub fn validate_title(task_name: &str) -> Result<String, Error> {
    let root = getroot();
    let filename = format!("{}/{}.yaml", root, task_name);
    if Path::new(&filename).is_file() {
        return Err(Error::new(
            ErrorKind::Other,
            "Task with same name already exists",
        ));
    }
    if has_spl_chars(task_name) {
        return Err(Error::new(
            ErrorKind::Other,
            "Please do not use the following special characters ! @ # $ % ^ & * ( ) , + . ? [ ] in task-name",
        ));
    }

    Ok(String::from(task_name))
}
