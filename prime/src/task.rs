use colored::Colorize;
use serde::{Deserialize, Serialize};
use std::env;
use std::fs::{write, DirBuilder};
use std::path::Path;
use std::process;

#[derive(Serialize, Deserialize, Debug)]
pub struct Task {
    pub title: String,
    pub deadline: String,
    pub priority: u8,
}

pub fn getroot() -> String {
    let root = match env::var("PRIME_ROOT") {
        Ok(r) => r,
        Err(e) => {
            eprintln!("Error: {}\n{}\n\n{}",e,
                        String::from("Please set the environment variable PRIME_ROOT to the directory where you want to save the tasks.").blue().bold(),
                        String::from("help:export PRIME_ROOT=<DIRECTORY_PATH>").red().bold());
            process::exit(1);
        }
    };
    root
}

pub fn checkandcreateroot() {
    let root = getroot();
    if !Path::new(&root).is_dir() {
        match DirBuilder::new().create(&root) {
            Ok(r) => r,
            Err(e) => {
                eprintln!(
                    "Error: {}\n{}",
                    e,
                    String::from(
                        "The $PRIME_ROOT Directory was not found and could not be created!"
                    )
                    .blue()
                    .bold()
                );
                process::exit(1);
            }
        };
    }
}

pub fn taskexists(task_name: &str) -> bool {
    let root = getroot();
    let filename = format!("{}/{}.yaml", &root, task_name);
    if Path::new(&filename).is_file() {
        return true;
    }
    return false;
}

pub fn writetask(task_name: String, deadline: String, priority: u8) {
    let root = getroot();
    checkandcreateroot();
    let filename = format!("{}/{}.yaml", &root, task_name);
    match write(
        filename,
        match serde_yaml::to_string(&Task {
            title: task_name.to_owned(),
            deadline: deadline.to_owned(),
            priority,
        }) {
            Ok(s) => s,
            Err(e) => {
                eprintln!(
                    "Error: {}\n{}",
                    e,
                    String::from("Serde couldn't parse the task").blue().bold()
                );
                process::exit(1);
            }
        },
    ) {
        Ok(_) => (),
        Err(e) => {
            eprintln!(
                "Error: {}\n{}",
                e,
                String::from("The task could not be created!").blue().bold()
            );
            process::exit(1);
        }
    };
}
