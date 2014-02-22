#!/usr/bin/python
import argparse
import random
import sys

"""A simple python program for solving Mastermind
(probably a registered trademark of someone or other, used without permission,
no endorsement expressed or implied).

The game involves one player secretly choosing 4 pegs from 6 colors, and the other player
iteratively attempting to guess the secret pattern. For each guess, the guess gets
feedback in the form of zero or more red pegs (saying that the guess has the right color
in the right location) and zero or more white pegs (saying that the right color is
present, but in the wrong location).

While playing, the question arose whether you could always win with less than 8 moves by
the simple and naive strategy of only playing moves that are consistent with the responses
thus far. I wrote this script to check that question.

In actuality, the most naive strategy (picking the lexicographically first answer that is
consistent with responses thus far) sometimes takes 9 guesses to arrive at the solution,
but a random guesser generally does much better, and the "best" guesser (trying to pick a
possibly-correct guess that will maximize information from the response) never needs more
than 6 guesses.
""" 

COLORS = 6
PINS = 4

def allPatterns():
  """Generator function to yield all possible color combinations"""
  cur = [0] * PINS
  while True:
    yield tuple(cur)
    for i in range(PINS):
      cur[i] += 1
      if cur[i] < COLORS:
        break
      cur[i] = 0
      if i == PINS - 1:
        return

def check(answer, probe):
  """Given an answer and a guess, return a score of (red, white)"""
  acolcnt = [0] * COLORS
  pcolcnt = [0] * COLORS
  
  red = 0
  for (a, p) in zip(answer, probe):
    if a == p:
      red = red + 1
    else:
      acolcnt[a] += 1
      pcolcnt[p] += 1
  white = 0
  for a, p in zip(acolcnt, pcolcnt):
    white += min(a, p)
  return (red, white)

def possibleAnswers(prevRounds):
  """Returns an iterable of all patterns which are consistent with responses to guesses thus far, provided as an array of (guess, (red, white))"""
  pr = tuple(prevRounds)
  return (candidate for candidate in allPatterns() if all((check(candidate, probe) == result for (probe, result) in pr)))

def randomPattern():
  """Select a random pattern"""
  return tuple((random.randint(0, COLORS - 1) for i in range(PINS)))

def chooseFirst(answers):
  """Pick the first response in the iterable answers"""
  guess = answers.next()
  answersCount = lambda: len(list(answers)) + 1
  return (guess, answersCount)

def choosePolychrome(answers):
  """Prefer answers which use a lot of colors as a simple improvement over monochrome guesses"""
  allAnswers = list(answers)
  bestGuess = None
  bestColorCount = 0
  for guess in allAnswers:
    colorsUsed = [False] * COLORS
    for pinColor in guess:
      colorsUsed[pinColor] = True
    colorCount = sum(colorsUsed)
    if colorCount > bestColorCount:
      bestGuess = guess
      bestColorCount = colorCount
    if bestColorCount == PINS:
      break # shortcut
  return (bestGuess, lambda: len(allAnswers))

def chooseBest(answers):
  """Pick the best guess: the one that is likely to give the most information in its response
     (measured by it having the smallest peak in response concentration)"""
  allAnswers = list(answers)
  bestGuess = None
  bestScore = Math.pow(COLORS, PINS)
  bestResults = {}
  for guess in allAnswers:
    results = {}
    for possibleAnswer in allAnswers:
      possibleResult = check(possibleAnswer, guess)
      results[possibleResult] = 1 + results.get(possibleResult, 0)
    score = max(results.values())
    if score < bestScore:
      bestGuess = guess
      bestScore = score
      bestResults = results
  return (bestGuess, lambda: len(allAnswers))

def chooseWorst(answers):
  """Pick the worst guess"""
  allAnswers = list(answers)
  worstGuess = None
  worstScore = 0
  worstResults = {}
  for guess in allAnswers:
    results = {}
    for possibleAnswer in allAnswers:
      possibleResult = check(possibleAnswer, guess)
      results[possibleResult] = 1 + results.get(possibleResult, 0)
    score = max(results.values())
    if score > worstScore:
      worstGuess = guess
      worstScore = score
      worstResults = results
  return (worstGuess, lambda: len(allAnswers))

def chooseRandom(answers):
  """Pick a possibly correct answer at random"""
  allAnswers = list(answers)
  guess = random.choice(allAnswers)
  return (guess, lambda: len(allAnswers))
  
def play(answer, chooser, onRound = None):
  """Play Mastermind once with the given answer and chooser"""
  rounds = []
  
  while 1:
    answers = possibleAnswers(rounds)
    (guess, answersCount) = chooser(answers)
    (red, white) = check(answer, guess)
    rounds.append((guess, (red, white)))
    if onRound:
      onRound(rounds, answersCount())
    if red == PINS:
      break
  
  return rounds

def printRound(rounds, answerCount):
  """Output info about this guess & result"""
  guess, (red, white) = rounds[-1]
  print "Round %d: %5d possible, guessed [%s], got %d red, %d white" % (len(rounds), answerCount, " ".join(map(str,guess)), red, white)

def playOnce(chooser):
  """Play a single game with a random answer with a provided choosing strategy"""
  answer = randomPattern()
  play(answer, chooser, onRound = printRound)

def playAll(chooser):
  """Play a game for every possible answer with a provided choosing strategy, accumulating
  and printing a summary of the outcomes"""
  results = {}
  for answer in allPatterns():
    rounds = play(answer, chooser)
    r = len(rounds)
    results[r] = 1 + results.get(r, 0)
  print "Rounds: Trials"
  for r in sorted(results.keys()):
    print "%-6d: %d" % (r, results[r])

# Choosing strategies
CHOICES = {
  'first': chooseFirst,
  'best': chooseBest,
  'worst': chooseWorst,
  'random': chooseRandom,
  'polychrome': choosePolychrome
}
CHOICES_HELP = ", ".join(sorted(CHOICES.keys()))

def choiceType(arg):
  """Validate --choose arguments"""
  if arg in CHOICES:
    return CHOICES[arg]
  raise argparse.ArgumentTypeError("%s is unknown: valid choosers are [%s]" % 
    (arg, CHOICES_HELP))

def main(argv = None):
  global COLORS, PINS

  if argv is None:
    argv = sys.argv
  
  parser = argparse.ArgumentParser(description='Play Mastermind')
  parser.add_argument('--choose', type=choiceType, default=chooseFirst,
                      help='How to choose a move, one of [%s]' % CHOICES_HELP)
  parser.add_argument('--all', dest='action', action='store_const',
                      const=playAll, default=playOnce,
                      help='enumerate and summarize all Mastermind games')
  parser.add_argument('--colors', type=int, default=COLORS, help='Number of different colors each pin can have')
  parser.add_argument('--pins', type=int, default=PINS, help='Number of pins in the secret pattern')
  args = parser.parse_args(argv[1:])
  COLORS = args.colors
  PINS = args.pins
  
  args.action(chooser = args.choose)
  return 0

if __name__ == "__main__":
  sys.exit(main())
