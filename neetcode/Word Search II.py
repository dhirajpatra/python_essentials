"""
Given a 2-D grid of characters board and a list of strings words, return all words that are present in the grid.

For a word to be present it must be possible to form the word with a path in the board with horizontally or
vertically neighboring cells. The same cell may not be used more than once in a word.

Example 1:
Input:
board = [
  ["a","b","c","d"],
  ["s","a","a","t"],
  ["a","c","k","e"],
  ["a","c","d","n"]
],
words = ["bat","cat","back","backend","stack"]

Output: ["cat","back","backend"]
Example 2:
Input:
board = [
  ["x","o"],
  ["x","o"]
],
words = ["xoxo"]

Output: []
Constraints:

1 <= board.length, board[i].length <= 12
board[i] consists only of lowercase English letter.
1 <= words.length <= 30,000
1 <= words[i].length <= 10
words[i] consists only of lowercase English letters.
All strings within words are distinct.
"""
class Solution:
    def findWords(self, board: List[List[str]], words: List[str]) -> List[str]:
        # Create a trie from the list of words
        trie = {}
        for word in words:
            node = trie
            for char in word:
                if char not in node:
                    node[char] = {}
                node = node[char]
            node['#'] = word  # Mark the end of a word

        ROWS, COLS = len(board), len(board[0])
        found_words = set()
        path = set()

        def dfs(r, c, node):
            if '#' in node:
                found_words.add(node['#'])
            if min(r, c) < 0 or r >= ROWS or c >= COLS or (r, c) in path or board[r][c] not in node:
                return
            path.add((r, c))
            char = board[r][c]
            dfs(r + 1, c, node[char])
            dfs(r - 1, c, node[char])
            dfs(r, c + 1, node[char])
            dfs(r, c - 1, node[char])
            path.remove((r, c))

        for r in range(ROWS):
            for c in range(COLS):
                if board[r][c] in trie:
                    dfs(r, c, trie)

        return list(found_words)

if __name__ == "__main__":
    solution = Solution()
    board1 = [
        ["a","b","c","d"],
        ["s","a","a","t"],
        ["a","c","k","e"],
        ["a","c","d","n"]
    ]
    words1 = ["bat","cat","back","backend","stack"]
    print(solution.findWords(board1, words1))  # Expected output: ["cat","back","backend"]

    board2 = [
        ["x","o"],
        ["x","o"]
    ]
    words2 = ["xoxo"]
    print(solution.findWords(board2, words2))  # Expected output: []