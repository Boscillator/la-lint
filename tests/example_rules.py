from lalint.matcher import RegexMatcher

disallow = {
    'the_letter_a': RegexMatcher('a')
}

require = {
    'the_letter_b': RegexMatcher('b')
}