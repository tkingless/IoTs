let data = 0
input.onButtonPressed(Button.A, () => {
    serial.writeString("Hello World")
    basic.pause(2000)
})
data = 0
serial.redirect(
SerialPin.P0,
SerialPin.P1,
BaudRate.BaudRate115200
)
