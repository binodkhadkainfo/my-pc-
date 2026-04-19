#include <iostream>
#include <string>
#include <cstdlib>

std::string monitor = "DP-1"; // your monitor

void rotate(int angle) {
   int transform = 0;

   if (angle == 0) transform = 0;
   else if (angle == 90) transform = 1;
   else if (angle == 180) transform = 2;
   else if (angle == 270) transform = 3;

   std::string cmd =
       "hyprctl keyword monitor " + monitor +
       ",preferred,auto,1,transform," + std::to_string(transform);

   int result = system(cmd.c_str());

   if (result == 0)
       std::cout << "✔ Rotated to " << angle << " degrees\n";
   else
       std::cout << "❌ Rotation failed\n";
}

int main() {
   std::cout << "Hyprland Screen Rotator\n";
   std::cout << "1: Normal (0)\n";
   std::cout << "2: Right (270)\n";
   std::cout << "3: Left (90)\n";
   std::cout << "4: Upside (180)\n";
   std::cout << "Choose option: ";

   int choice;
   std::cin >> choice;

   switch(choice) {
       case 1: rotate(0); break;
       case 2: rotate(270); break;
       case 3: rotate(90); break;
       case 4: rotate(180); break;
       default: std::cout << "Invalid option\n";
   }

   return 0;
}
