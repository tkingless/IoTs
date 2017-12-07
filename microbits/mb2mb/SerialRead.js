let data = ""
serial.redirect(
SerialPin.P0,
SerialPin.P1,
BaudRate.BaudRate115200
)
basic.forever(() => {
    data = serial.readString()
    basic.showString(data)
    basic.pause(2000)
})
