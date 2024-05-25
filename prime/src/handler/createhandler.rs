use crate::task::writetask;
use crate::{
    args::CreateArgs,
    parser::parsedeadline,
    validation::{validate_priority, validate_title},
};
use std::io::Error;

pub fn handle(args: CreateArgs) -> Result<(), Error> {
    let priority = validate_priority(args.priority)?;
    let deadline = parsedeadline(&args.deadline)?.to_string();
    let task_name = validate_title(&args.task_name)?;
    writetask(task_name, deadline, priority);
    Ok(())
}
