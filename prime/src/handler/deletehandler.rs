use crate::{
    args::DeleteArgs,
    task::{getroot, taskexists},
};
use std::fs;
use std::io::{Error, ErrorKind};
pub fn handle(args: DeleteArgs) -> Result<(), Error> {
    let root = getroot();
    if taskexists(&args.task_name) {
        let oldfile = format!("{}/{}.yaml", &root, &args.task_name);
        let newfile;
        if args.archive {
            fs::create_dir_all(&format!("{}/archive/complete", &root))?;
            fs::create_dir_all(&format!("{}/archive/incomplete", &root))?;
            if args.done {
                newfile = format!("{}/archive/complete/{}.yaml", &root, &args.task_name);
            } else {
                newfile = format!("{}/archive/incomplete/{}.yaml", &root, &args.task_name);
            }
            fs::rename(oldfile, newfile)?;
        } else {
            fs::remove_file(oldfile)?;
        }
        Ok(())
    } else {
        Err(Error::new(ErrorKind::Other, "No such task exists!"))
    }
}
