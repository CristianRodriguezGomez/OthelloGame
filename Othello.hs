import Graphics.UI.Gtk

main :: IO ()
main = do
    -- Inicializa GTK
    initGUI

    -- Crea la ventana
    window <- windowNew
    set window [windowTitle := "Othello", windowDefaultWidth := 400, windowDefaultHeight := 400]

    -- Crea un contenedor de tipo grid para el tablero
    grid <- gridNew

    -- Crear 64 botones para el tablero 8x8
    buttons <- mapM (const (buttonNewWithLabel " ")) (replicate 64 ())

    -- Organiza los botones en una grilla 8x8
    let rows = 8
        cols = 8
    forM_ [0..rows-1] $ \r -> 
        forM_ [0..cols-1] $ \c -> 
            gridAttach grid (buttons !! (r * cols + c)) c r 1 1

    -- Añadir la grilla a la ventana
    containerAdd window grid

    -- Mostrar la ventana y su contenido
    widgetShowAll window

    -- Manejar el cierre de la ventana
    on window objectDestroy mainQuit

    -- Inicia el loop principal de GTK
    mainGUI
