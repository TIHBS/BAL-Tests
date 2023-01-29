pub contract Example {

    pub event StringUpdate(oldValue: String, newValue: String)

    pub var greeting: String

    pub fun getString(): String {
        return self.greeting
    }

    pub fun setValues(name: String) : Void {
        emit StringUpdate(oldValue: self.greeting, newValue: name);

        self.greeting = name;

    }

    init() {
        self.greeting = "Hello World!"
    }

}