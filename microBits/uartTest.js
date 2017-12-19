let readData = ""
input.onButtonPressed(Button.A, () => {
    serial.writeString("W")
})
serial.redirect(
SerialPin.P0,
SerialPin.P1,
BaudRate.BaudRate9600
)
basic.forever(() => {
    readData = serial.readString()
    if (!(readData == "")) {
        basic.showString(readData)
    }
    basic.pause(2000)
})
