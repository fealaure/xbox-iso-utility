def get_logger(widget):
    def log(msg):
        widget.insert("end", msg + "\n")
        widget.see("end")
        widget.update()
    return log
