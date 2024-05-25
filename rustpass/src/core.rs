use helper::gen_char_set;
use helper::shuffle_char_set;

use crate::args::RustPassArgs;

pub fn foo(args: &RustPassArgs) {
    let mut char_set: Vec<u8> = gen_char_set(&args);
    for i in &char_set {
        print!("{}", *i as char);
    }
    println!();

    shuffle_char_set(&mut char_set, args.seed);
    for i in &char_set {
        print!("{}", *i as char);
    }
    println!();
}

pub mod helper;
