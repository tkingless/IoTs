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
            basic.pause(300)
            basic.showLeds(`
                . . . . .
                . . # . .
                . # # # .
                . . # . .
                . . . . .
                `)
            basic.pause(500)
            basic.showLeds(`
                . . # . .
                . # . # .
                . # # . .
                . # # # .
                . . # . .
                `)
        }
        if (readData == "A") {
            for (let i = 0; i < 4; i++) {
                basic.showLeds(`
                    . . . # .
                    . # # . .
                    # . # . #
                    # # # # #
                    . # # # .
                    `)
                basic.pause(100)
                basic.showLeds(`
                    . . # . .
                    . # . # .
                    # # # # #
                    # . # . #
                    . # # # .
                    `)
                basic.pause(100)
                basic.showLeds(`
                    . # . . .
                    . . # # .
                    # . # . #
                    # # # # #
                    . # # # .
                    `)
                basic.pause(100)
                basic.showLeds(`
                    . . # . .
                    . # # # .
                    # # # # #
                    # . # . #
                    . # # # .
                    `)
                basic.pause(100)
            }
        }
        if (readData == "H") {
            for (let i = 0; i < 4; i++) {
                basic.showLeds(`
                    . . . . .
                    . . . . .
                    . . # . .
                    . . . . .
                    . . . . .
                    `)
                basic.pause(200)
                basic.showLeds(`
                    . . . . .
                    . . # . .
                    . # # # .
                    . . # . .
                    . . . . .
                    `)
                basic.pause(200)
                basic.showLeds(`
                    # . # . #
                    . # # . .
                    # # . # #
                    . # # # .
                    # . # . #
                    `)
                basic.pause(200)
                basic.showLeds(`
                    . . . . .
                    . . # . .
                    . # # # .
                    . . # . .
                    . . . . .
                    `)
            }
        }
        if (readData == "S") {
            basic.pause(100)
            basic.showLeds(`
                . . . . .
                . . # . .
                . # # # .
                . . # . .
                . . . . .
                `)
            basic.pause(100)
            basic.showLeds(`
                . . . # .
                . . # . .
                . # # # #
                . . # . .
                . . . # .
                `)
            basic.pause(500)
        }
    }
})
