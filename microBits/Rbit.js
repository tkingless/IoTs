let readData = ""
input.onButtonPressed(Button.A, () => {
    
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
                . . . . .
                . . . . .
                . # # # .
                . . . . .
                . . . . .
                `)
            basic.showLeds(`
                . . . . .
                . . # . .
                . # # # .
                . . # . .
                . . . . .
                `)
            basic.pause(300)
            basic.showLeds(`
                . . # . .
                . # . # .
                . # # . .
                . # # # .
                . . # . .
                `)
        }
        if (readData == "A") {
            for (let i = 0; i < 3; i++) {
                basic.showLeds(`
                    . . . # .
                    . # # . .
                    # . # # .
                    # # # # #
                    . # # # .
                    `)
                basic.showLeds(`
                    . . # . .
                    . # . # .
                    # # . # #
                    # . # . #
                    . # # # .
                    `)
                basic.showLeds(`
                    . # . . .
                    . . # # .
                    . # # . #
                    # # # # #
                    . # # # .
                    `)
                basic.showLeds(`
                    . . # . .
                    . # . # .
                    # # . # #
                    # . # . #
                    . # # # .
                    `)
            }
        }
        if (readData == "H") {
            basic.showLeds(`
                . . . . .
                . # # # .
                # # . # #
                # . . . #
                . . . . .
                `)
        }
        if (readData == "S") {
            basic.showLeds(`
                . . . . .
                . . . # .
                . . # # #
                . . . # .
                . . # . .
                `)
            basic.showLeds(`
                . . . . .
                . . . # .
                . # # # #
                . . . # .
                . . # . .
                `)
            basic.showLeds(`
                . . # . .
                . . . # .
                . # # # #
                # . . # .
                . . # . .
                `)
            basic.showLeds(`
                . . # . .
                . . . # .
                . # # # #
                # . . # .
                . . # . .
                `)
            basic.showLeds(`
                . # # . .
                . . . # .
                . # # # #
                # . . # .
                . . # . .
                `)
        }
    }
})
