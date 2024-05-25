#[cfg(test)]
use crate::{args::CreateArgs, handler::createhandler};

#[test]
pub fn populate() {
    createhandler::handle(CreateArgs {
        task_name: String::from("make-app"),
        deadline: String::from("2-h"),
        priority: 0,
    })
    .unwrap();
    createhandler::handle(CreateArgs {
        task_name: String::from("make-lunch"),
        deadline: String::from("2-w"),
        priority: 1,
    })
    .unwrap();
    createhandler::handle(CreateArgs {
        task_name: String::from("lunch-task"),
        deadline: String::from("2-d"),
        priority: 2,
    })
    .unwrap();
    createhandler::handle(CreateArgs {
        task_name: String::from("file books"),
        deadline: String::from("10-h"),
        priority: 3,
    })
    .unwrap();
    createhandler::handle(CreateArgs {
        task_name: String::from("search-stuff"),
        deadline: String::from("2023-03-25"),
        priority: 1,
    })
    .unwrap();

    createhandler::handle(CreateArgs {
        task_name: String::from("buy-gift"),
        deadline: String::from("2023-05-20"),
        priority: 2,
    })
    .unwrap();
}
