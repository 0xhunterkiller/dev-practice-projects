mod args;
mod core;

use args::RustPassArgs;
use clap::Parser;

use rpassword;

use argon2::Argon2;
use sha2::{Digest, Sha256};

fn main() {
    let args = RustPassArgs::parse();
    let mpass = rpassword::prompt_password(&String::from("Master Password: ")).unwrap();

    core::foo(&args);

    println!("Username: {}", args.username);
    println!("service: {}", args.service);
    println!("mpass: {}", mpass);

    println!("len: {}", args.len);
    println!("seed: {}", args.seed);

    let salt: String = [
        args.username.as_str(),
        args.service.as_str(),
        args.seed.to_string().as_str(),
    ]
    .concat();
    println!("salt: {}", salt);

    let mut temp = Sha256::new();
    temp.update(&salt.as_bytes());
    let salty = temp.finalize();

    let mut op_key = [0u8; 32];
    Argon2::default()
        .hash_password_into(mpass.as_bytes(), &salty[..], &mut op_key)
        .expect("Something went wrong!");

    for b in salty {
        print!("{b:02x}")
    }
    println!();
    for x in op_key {
        print!("{x:02x}");
    }
    println!();
}
