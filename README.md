# MiniLanding3D

![ss2](https://user-images.githubusercontent.com/80536083/178206863-ddb0a249-2058-405b-9c69-7803f6b7d4e4.PNG)
![ss1](https://user-images.githubusercontent.com/80536083/178206882-6c13291c-bcac-4ce0-9886-283369e2ebe7.PNG)


miniLanding3D is a spaceflight simulation game in which
you take control of a lunar lander at the final phases
of its landing burn. You will have to cancel your velocity
and make a soft touchdown before you run out of propellant.

## Required Python Modules

 - pyopengl
 - pygame
 - pywavefront
 - keyboard

## How To Run

a) Running main_ext_view.py starts the game in external 
   view (third person) mode.
   
b) Running main_cabin_view.py starts the game in commander's
   POV, looking out of the lander's window

## Controls

-  W, A, S, D, Q, E keys to adjust angular velocity (via
   reaction control thruster pulses)
   
-  U & J keys to respectively increase and decrease throttle
   (throttle below about 17% is not allowed since it would be
   impossible to sustain combustion)
   
-  T & G keys to respectively activate and deactivate
   descent-rate autothrottle
   
-  Y & H keys to respectively increase and decrease autothrottle
   descent-rate setting
   
-  R & F keys to respectively start and shutdown the main
   engine
   
-  Hold the X key to kill all rotation (panic button)

-  M key toggles music.
