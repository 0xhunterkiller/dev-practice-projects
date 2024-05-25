use clap::{ArgAction, Args, Parser, Subcommand};

#[derive(Parser, Debug)]
#[command(
    author = "Saai Sudarsanan",
    version = "1.0.0",
    about = "A CLI based To Do App"
)]
#[command(propagate_version = true)]
pub struct PrimeArgs {
    #[command(subcommand)]
    pub command: Mode,
}

#[derive(Subcommand, Debug)]
pub enum Mode {
    /// Create a new task
    Create(CreateArgs),
    /// Show Tasks (default : Last 20 tasks)
    Read(ReadArgs),
    /// Update a task
    Update(UpdateArgs),
    /// Mark as Complete / Delete a task
    Delete(DeleteArgs),
}

#[derive(Args, Debug)]
pub struct CreateArgs {
    /// The task title (No Special Characters)
    #[arg(value_name = "TASK NAME")]
    pub task_name: String,
    /// Can be of the form t-x
    ///
    /// - x is the unit of time in consideration. [can be w,d,m,h or s]
    ///
    /// - t is the number of units of the x specified.
    ///
    /// Example :
    ///
    /// 2-w -> 2 Weeks | 5-d -> 5 Days | 3-h -> 3 Hours | 10-m -> 10 Minutes | 15-s -> 15 Seconds
    ///
    /// Or a date of the format -> yyyy-mm-dd
    #[arg(value_name="DEADLINE",default_value_t=String::from("2-d"))]
    pub deadline: String,

    /// Priority of this task (0 <= p < 4)
    #[arg(value_name = "PRIORITY", default_value_t = 0)]
    pub priority: u8,
}

#[derive(Debug, Args)]
pub struct ReadArgs {
    /// Filter by title
    #[arg(long = "title", short = 't', value_name = "TASK NAME")]
    pub task_name: Option<String>,

    /// Filter by deadline
    #[arg(long = "deadline", short = 'd', value_name = "DEADLINE")]
    pub deadline: Option<String>,

    /// Filter by priority
    #[arg(long = "priority", short = 'p', value_name = "PRIORITY")]
    pub priority: Option<u8>,

    /// Change count value
    #[arg(
        long = "count",
        short = 'c',
        value_name = "MAX COUNT",
        default_value_t = 20
    )]
    pub count: i32,
}

#[derive(Args, Debug)]
pub struct UpdateArgs {
    /// Title of the task you want to update
    #[arg(value_name = "TASK NAME")]
    pub task_name: String,

    /// New Title
    #[arg(long = "newtitle", short = 't', value_name = "NEW TASK NAME")]
    pub new_task_name: Option<String>,

    /// New Deadline
    #[arg(long = "newdeadline", short = 'd', value_name = "NEW DEADLINE")]
    pub new_deadline: Option<String>,

    /// New Priority
    #[arg(long = "newpriority", short = 'p', value_name = "NEW PRIORITY")]
    pub new_priority: Option<u8>,
}

#[derive(Args, Debug)]
pub struct DeleteArgs {
    /// The Title of the task you want to delete
    #[arg(value_name = "TASK NAME")]
    pub task_name: String,
    /// Have you finished this task?
    #[arg(long="done",short='k',value_name="DONE?",action=ArgAction::SetTrue)]
    pub done: bool,
    /// Do you want to archive this task?
    #[arg(long="dont_archive",short='x',value_name="ARCHIVE?",action=ArgAction::SetFalse)]
    pub archive: bool,
}
