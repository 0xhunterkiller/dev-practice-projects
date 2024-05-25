use clap::Parser;
use colored::Colorize;
use prime::args::{Mode, PrimeArgs};
use prime::handler::{createhandler, deletehandler, readhandler, updatehandler};
use std::process;
fn main() {
    let opts = PrimeArgs::parse();
    match opts.command {
        Mode::Create(args) => {
            match createhandler::handle(args) {
                Ok(r) => r,
                Err(e) => {
                    eprintln!(
                        "{} {}",
                        String::from("Error executing your request: ").red().bold(),
                        e
                    );
                    process::exit(1);
                }
            };
        }
        Mode::Read(args) => {
            match readhandler::handle(args) {
                Ok(r) => r,
                Err(e) => {
                    eprintln!(
                        "{} {}",
                        String::from("Error executing your request: ").red().bold(),
                        e
                    );
                    process::exit(1);
                }
            };
        }
        Mode::Update(args) => {
            match updatehandler::handle(args) {
                Ok(r) => r,
                Err(e) => {
                    eprintln!(
                        "{} {}",
                        String::from("Error executing your request: ").red().bold(),
                        e
                    );
                    process::exit(1);
                }
            };
        }
        Mode::Delete(args) => {
            match deletehandler::handle(args) {
                Ok(r) => r,
                Err(e) => {
                    eprintln!(
                        "{} {}",
                        String::from("Error executing your request: ").red().bold(),
                        e
                    );
                    process::exit(1);
                }
            };
        }
    }
}
