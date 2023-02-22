# MyLogger
Another Logger implementation in Python. This one fits my needs because it's highly customizable and I adore to log oin multiple ways for important stuff

## Usage

See MyLogger/example.py for an example usage

It's not designed to be out-of-the-box by obfuscating the complexity. Because it will lake flexibility.
But it's designed to be as higly customizable while staying straitforward.

## Features

### Where can it log
- Log on notification system of linux, with "notify-gui" shell tool
- Log to journalctl, with "logger" shell tool
- Log to a file, with custom rotating options
- Or anywhere you want, thanks to a design which can be easily extended to fit your needs

### How can it log
- Logging with event-driven principle : create as many context of logging you want
- You won't get bloat with a persistent and static logger object and its child. Instead your logger is a class instance (much more pythonic !)
- Each context can be associated with specific place to log, or different log formatting
- Easily handle your log as a file, with any handler compatible with "open" function (useful for logging subprocess output)

I recommend to use this module by defining a global logger variable common to all files inside a project (Yes globals are the darkness, but a logger is a special kind of toy)

### Will this be improve ?

According to my needs and time, I could add :
- logging to mail
- decorator for functions (exception catching)
- add **kwargs to log function
- add a class where FileHandler and all FileRotators are merged for a more intuitive usage
