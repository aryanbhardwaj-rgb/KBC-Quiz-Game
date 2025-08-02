# KBC-Quiz-Game
A feature-rich Python quiz app inspired by Kaun Banega Crorepati (KBC), built with Tkinter and enhanced with sound, images, and lifelines.
Supports full screen, min/max controls, a welcoming start screen with music, dynamic timer, flip questions, and much more.
Features
	•	Start Screen with background music and a KBC welcome graphic.
	•	Full KBC Quiz Interface:
	•	Question area, four answer options, lifeline buttons, prize ladder.
	•	Timer for first 10 questions (45s each), then unlimited time.
	•	Clean, centered UI that looks great on Windows and Mac.
	•	Lifelines: 50:50, Audience Poll, Phone a Friend, and Flip Question.
 •	Audio and Visual Polish:
	•	Custom popups for feedback/win/game over.
	•	Switch full-screen/minimize during the quiz.
	•	Random and tricky science & logic questions!
 
Getting Started
1. Clone the repository:
   git clone https://github.com/yourusername/kbc-quiz-game.git
cd kbc-quiz-game

3. Install requirements:
   pip install pillow pygame

   3. Assets:
	•	Place your start screen image as  assets/screen.jpg  (recommended: 800x450px).
	•	Place your start screen audio in the project root as  audio.mp3 .
	•	Place your KBC logo as  kbc_logo.png  in the project root.
4. Run the game:
   python kbc_quiz.py

Controls
	•	Navigate: Mouse only! Select your option, click “Lock Kar Diya Jaye”.
	•	Lifelines: Click any enabled lifeline once per game.
	•	Timer: 45 seconds per question for the first 10 questions.
	•	Window: Use top-right buttons in quiz to Fullscreen or Minimize.
 
Customization
	•	Add your own questions by editing the  QUESTIONS  and  FLIP_QUESTIONS  lists in  kbc_quiz.py .
	•	Change styling/colors/fonts by editing widget parameters in the code.

Controls
	•	Navigate: Mouse only! Select your option, click “Lock Kar Diya Jaye”.
	•	Lifelines: Click any enabled lifeline once per game.
	•	Timer: 45 seconds per question for the first 10 questions.
	•	Window: Use top-right buttons in quiz to Fullscreen or Minimize.
 
Customization
	•	Add your own questions by editing the  QUESTIONS  and  FLIP_QUESTIONS  lists in  kbc_quiz.py .
	•	Change styling/colors/fonts by editing widget parameters in the code.

Credits
	•	Tkinter for UI
	•	Pillow for image handling
	•	pygame for audio playback
Logo and image assets used only for demonstration.

Enjoy playing—and best of luck. Lock kar diya jaaye!
