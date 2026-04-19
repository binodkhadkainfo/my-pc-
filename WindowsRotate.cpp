#include <windows.h>
#include <iostream>

// Define missing constants if needed
#ifndef DM_DISPLAYORIENTATION
#define DM_DISPLAYORIENTATION 0x00000080
#endif

#ifndef DMDO_DEFAULT
#define DMDO_DEFAULT 0
#define DMDO_90      1
#define DMDO_180     2
#define DMDO_270     3
#endif

bool RotateScreen(int angle) {
    DEVMODE dm;
    ZeroMemory(&dm, sizeof(dm));
    dm.dmSize = sizeof(dm);

    if (!EnumDisplaySettings(NULL, ENUM_CURRENT_SETTINGS, &dm)) {
        std::cerr << "❌ Failed to get display settings.\n";
        return false;
    }

    dm.dmFields = DM_DISPLAYORIENTATION | DM_PELSWIDTH | DM_PELSHEIGHT;

    int newOrientation;

    switch (angle) {
        case 0:   newOrientation = DMDO_DEFAULT; break;
        case 90:  newOrientation = DMDO_270; break;
        case 180: newOrientation = DMDO_180; break;
        case 270: newOrientation = DMDO_90; break;
        default:
            return false;
    }

    // Set resolution for rotation
    if (angle == 90 || angle == 270) {
        dm.dmPelsWidth = 1440;
        dm.dmPelsHeight = 2560;
    } else {
        dm.dmPelsWidth = 2560;
        dm.dmPelsHeight = 1440;
    }

    dm.dmDisplayOrientation = newOrientation;

    LONG result = ChangeDisplaySettingsEx(NULL, &dm, NULL, CDS_UPDATEREGISTRY | CDS_RESET, NULL);
    return (result == DISP_CHANGE_SUCCESSFUL);
}

int main() {
    std::cout << "Press Win + Alt to activate rotation mode.\n";
    std::cout << "Then press an arrow key to rotate the screen once.\n";

    while (true) {
        // Check if Win + Alt pressed together to activate rotation mode
        bool winPressed = (GetAsyncKeyState(VK_LWIN) & 0x8000) || (GetAsyncKeyState(VK_RWIN) & 0x8000);
        bool altPressed = (GetAsyncKeyState(VK_MENU) & 0x8000);

        if (winPressed && altPressed) {
            std::cout << "Rotation mode activated. Press arrow key...\n";

            // Wait for user to press an arrow key
            while (true) {
                if (GetAsyncKeyState(VK_UP) & 0x8000) {
                    std::cout << "Rotating to 0° (normal)\n";
                    RotateScreen(0);
                    goto end_program;
                }
                else if (GetAsyncKeyState(VK_DOWN) & 0x8000) {
                    std::cout << "Rotating to 180° (upside down)\n";
                    RotateScreen(180);
                    goto end_program;
                }
                else if (GetAsyncKeyState(VK_LEFT) & 0x8000) {
                    std::cout << "Rotating to 90° (left)\n";
                    RotateScreen(90);
                    goto end_program;
                }
                else if (GetAsyncKeyState(VK_RIGHT) & 0x8000) {
                    std::cout << "Rotating to 270° (right)\n";
                    RotateScreen(270);
                    goto end_program;
                }
                Sleep(50);
            }
        }
        Sleep(50);
    }

end_program:
    std::cout << "Rotation done. Exiting program.\n";
    return 0;
}
