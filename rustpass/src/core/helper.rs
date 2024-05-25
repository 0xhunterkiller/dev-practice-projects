use crate::args::RustPassArgs;

use rand::{rngs::StdRng, seq::SliceRandom, SeedableRng};

pub fn gen_char_set(args: &RustPassArgs) -> Vec<u8> {
    let mut char_set: Vec<u8> = Vec::new();

    if args.digits {
        char_set.extend(b"1234567890");
    }

    if args.lowercase {
        char_set.extend(b"abcdefghijklmnopqrstuvwxyz");
    }

    if args.uppercase {
        char_set.extend(b"ABCDEFGHIJKLMNOPQRSTUVWXYZ");
    }

    if args.special_chars {
        char_set.extend(b"`~!@#$%^&*()_+-=[]{}\\|;:'\",./<>?");
    }

    return char_set;
}

pub fn shuffle_char_set(char_set: &mut [u8], seed: u64) {
    let mut rng = StdRng::seed_from_u64(seed);
    char_set.shuffle(&mut rng);
}
