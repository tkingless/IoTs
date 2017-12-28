let readData = ""
input.onButtonPressed(Button.A, () => {
    serial.writeString("W")
})
serial.redirect(
SerialPin.P0,
SerialPin.P1,
BaudRate.BaudRate115200
)
basic.forever(() => {
    readData = serial.readString()
    if (!(readData == "")) {
        if (readData == "N") {
            basic.showLeds(`
                . . # . .
                # # # # .
                # . # # .
                # # # # .
                . # # # .
                `)
            basic.showLeds(`
                . . . . .
                . . . . .
                # # # # .
                . . . . .
                . . . . .
                `)
            basic.pause(500)
            basic.showLeds(`
                . . # . .
                # # # # .
                # . # # .
                # # # # .
                . # # # .
                `)
        }
    }
})