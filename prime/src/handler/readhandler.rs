use crate::{
    args::ReadArgs,
    parser::parsedeadline,
    task::{getroot, Task},
    validation::has_spl_chars,
};
use chrono::{DateTime, Local};
use colored::Colorize;
use glob::glob;
use regex::Regex;
use std::fs;
use std::io::Error;
use std::process;

pub fn handle(args: ReadArgs) -> Result<(), Error> {
    let root = getroot();
    let entries: Vec<_> = glob(&format!("{}/*.yaml", &root)).unwrap().collect();
    let mut count = 0;
    for entry in entries {
        let filename = entry.unwrap().to_str().unwrap().to_owned();
        let task_contents = fs::read_to_string(&filename)?;
        let task: Task = match serde_yaml::from_str(&task_contents) {
            Ok(r) => r,
            Err(e) => {
                eprintln!("{}", e);
                process::exit(1);
            }
        };

        let mut tshow = false;
        let mut dshow = false;
        let mut pshow = false;

        // title check
        match &args.task_name {
            Some(q) => {
                if has_spl_chars(&q) {
                    eprintln!(
                        "{}",
                        String::from("query string cannot contain special characters").red()
                    );
                    process::exit(1);
                }
                let query = match Regex::new(&format!(r"{}", q)) {
                    Ok(r) => r,
                    Err(e) => {
                        eprintln!("{}", e);
                        process::exit(1);
                    }
                };
                if query.is_match(&task.title) {
                    tshow = true;
                }
            }
            None => {
                tshow = true;
            }
        }

        // deadline check
        match &args.deadline {
            Some(d) => {
                let dl = parsedeadline(d)?;
                if match task.deadline.parse::<DateTime<Local>>() {
                    Ok(r) => r,
                    Err(e) => {
                        eprintln!("{}", e);
                        process::exit(1);
                    }
                } < dl
                {
                    dshow = true;
                }
            }
            None => {
                dshow = true;
            }
        }

        // priority check
        match args.priority {
            Some(p) => {
                if task.priority == p {
                    pshow = true;
                }
            }
            None => {
                pshow = true;
            }
        }

        // count check
        if tshow && pshow && dshow {
            count += 1;
            if count > args.count {
                break;
            }
        }
        if tshow && pshow && dshow {
            println!("{}", task.title.red().bold());
            println!("{}", task.priority.to_string().blue());
            println!("{}", task.deadline.green());
        }
    }
    Ok(())
}
