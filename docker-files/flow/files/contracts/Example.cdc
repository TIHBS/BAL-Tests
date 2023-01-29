pub contract Example {

    pub event StringUpdate(oldValue: String, newValue: String)
    pub event BooleanUpdate(oldValue: Bool, newValue: Bool)
    pub event Int8Update(oldValue: Int8, newValue: Int8)
    pub event Unt128Update(oldValue: UInt128, newValue: UInt128)
    pub event AddressUpdate(oldValue: Address, newValue: Address)

    pub var greeting: String
    pub var booleanVar: Bool
    pub var int8Var: Int8
    pub var uint128Var: UInt128
    pub var addressVar: Address

    pub fun getString(): String {
        return self.greeting
    }

    pub fun setValues(name: String, newBooleanVar: Bool, newInt8Var: Int8, newUInt128Var: UInt128) : Void {
        emit StringUpdate(oldValue: self.greeting, newValue: name);
        emit BooleanUpdate(oldValue: self.booleanVar, newValue: newBooleanVar)
        emit Int8Update(oldValue: self.int8Var, newValue: newInt8Var)
        emit Unt128Update(oldValue: self.uint128Var, newValue: newUInt128Var)

        self.greeting = name;
        self.booleanVar = newBooleanVar;
        self.int8Var = newInt8Var;
        self.uint128Var = newUInt128Var;

    }

    pub fun setAddress(newAddress: Address) : Void {

        emit AddressUpdate(oldValue: self.addressVar, newValue: newAddress)
        self.addressVar = newAddress;

    }

    init() {
        self.greeting = "Hello World!"
        self.booleanVar = false
        self.int8Var = -1
        self.uint128Var = 100
        self.addressVar = 0x436164656E636521
    }

}