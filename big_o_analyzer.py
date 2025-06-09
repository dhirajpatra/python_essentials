import ast
from typing import Dict, List, Set, Tuple, Optional

class BigOAnalyzer:
    def __init__(self):
        self.complexity_patterns = {
            'O(1)': ['constant', 'single operation'],
            'O(log n)': ['binary search', 'tree traversal', 'divide and conquer'],
            'O(n)': ['linear search', 'single loop'],
            'O(n log n)': ['merge sort', 'heap sort', 'efficient sorting'],
            'O(n²)': ['nested loops', 'bubble sort', 'selection sort'],
            'O(n³)': ['triple nested loops'],
            'O(2^n)': ['recursive fibonacci', 'subset generation'],
            'O(n!)': ['permutation generation']
        }
    
    def analyze_code(self, code: str) -> Dict:
        """Main method to analyze code and return Big O estimation"""
        try:
            tree = ast.parse(code)
            analysis = {
                'estimated_complexity': 'O(1)',
                'confidence': 'Low',
                'reasons': [],
                'detailed_analysis': {},
                'suggestions': []
            }
            
            # Analyze the AST
            self._analyze_node(tree, analysis, depth=0)
            
            return analysis
            
        except SyntaxError as e:
            return {
                'error': f'Syntax error in code: {str(e)}',
                'estimated_complexity': 'Unknown',
                'confidence': 'None'
            }
    
    def _analyze_node(self, node: ast.AST, analysis: Dict, depth: int = 0, parent_loops: int = 0):
        """Recursively analyze AST nodes"""
        
        if isinstance(node, ast.FunctionDef):
            func_analysis = self._analyze_function(node)
            analysis['detailed_analysis'][node.name] = func_analysis
            
            # Update overall complexity based on function analysis
            if self._compare_complexity(func_analysis['complexity'], analysis['estimated_complexity']):
                analysis['estimated_complexity'] = func_analysis['complexity']
                analysis['reasons'].extend(func_analysis['reasons'])
        
        elif isinstance(node, (ast.For, ast.While)):
            loop_analysis = self._analyze_loop(node, parent_loops)
            
            if loop_analysis['nested_level'] >= 2:
                new_complexity = f"O(n^{loop_analysis['nested_level']})"
                if loop_analysis['nested_level'] == 2:
                    new_complexity = "O(n²)"
                elif loop_analysis['nested_level'] == 3:
                    new_complexity = "O(n³)"
                
                if self._compare_complexity(new_complexity, analysis['estimated_complexity']):
                    analysis['estimated_complexity'] = new_complexity
                    analysis['reasons'].append(f"Nested loops detected (depth: {loop_analysis['nested_level']})")
            
            # Recursively analyze loop body with increased parent_loops count
            for child in ast.iter_child_nodes(node):
                self._analyze_node(child, analysis, depth + 1, parent_loops + 1)
        
        elif isinstance(node, ast.Call):
            call_analysis = self._analyze_function_call(node)
            if call_analysis:
                analysis['reasons'].extend(call_analysis)
        
        else:
            # Continue traversing other nodes
            for child in ast.iter_child_nodes(node):
                self._analyze_node(child, analysis, depth, parent_loops)
    
    def _analyze_function(self, func_node: ast.FunctionDef) -> Dict:
        """Analyze a specific function"""
        analysis = {
            'complexity': 'O(1)',
            'reasons': [],
            'loop_depth': 0,
            'recursive_calls': 0,
            'has_sorting': False
        }
        
        # Check for recursion
        recursive_calls = self._count_recursive_calls(func_node)
        if recursive_calls > 0:
            analysis['recursive_calls'] = recursive_calls
            # Simple heuristic: if it looks like fibonacci-style recursion
            if recursive_calls >= 2:
                analysis['complexity'] = 'O(2^n)'
                analysis['reasons'].append('Multiple recursive calls detected (exponential)')
            else:
                analysis['complexity'] = 'O(n)'
                analysis['reasons'].append('Single recursive call detected (linear)')
        
        # Check loop nesting
        max_depth = self._get_max_loop_depth(func_node)
        analysis['loop_depth'] = max_depth
        
        if max_depth == 1:
            if analysis['complexity'] == 'O(1)':
                analysis['complexity'] = 'O(n)'
                analysis['reasons'].append('Single loop detected')
        elif max_depth == 2:
            analysis['complexity'] = 'O(n²)'
            analysis['reasons'].append('Double nested loops detected')
        elif max_depth >= 3:
            analysis['complexity'] = f'O(n^{max_depth})'
            analysis['reasons'].append(f'Nested loops with depth {max_depth}')
        
        # Check for sorting operations
        if self._has_sorting_operations(func_node):
            analysis['has_sorting'] = True
            if analysis['complexity'] in ['O(1)', 'O(n)']:
                analysis['complexity'] = 'O(n log n)'
                analysis['reasons'].append('Sorting operation detected')
        
        return analysis
    
    def _count_recursive_calls(self, func_node: ast.FunctionDef) -> int:
        """Count recursive calls within a function"""
        func_name = func_node.name
        count = 0
        
        for node in ast.walk(func_node):
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
                if node.func.id == func_name:
                    count += 1
        
        return count
    
    def _get_max_loop_depth(self, node: ast.AST) -> int:
        """Get maximum nesting depth of loops"""
        max_depth = 0
        
        def count_depth(n, current_depth=0):
            nonlocal max_depth
            if isinstance(n, (ast.For, ast.While)):
                current_depth += 1
                max_depth = max(max_depth, current_depth)
            
            for child in ast.iter_child_nodes(n):
                count_depth(child, current_depth)
        
        count_depth(node)
        return max_depth
    
    def _has_sorting_operations(self, node: ast.AST) -> bool:
        """Check for sorting operations"""
        sorting_functions = {'sort', 'sorted', 'heapify', 'nlargest', 'nsmallest'}
        
        for n in ast.walk(node):
            if isinstance(n, ast.Call):
                if isinstance(n.func, ast.Name) and n.func.id in sorting_functions:
                    return True
                elif isinstance(n.func, ast.Attribute) and n.func.attr in sorting_functions:
                    return True
        
        return False
    
    def _analyze_loop(self, loop_node: ast.AST, parent_loops: int) -> Dict:
        """Analyze loop characteristics"""
        return {
            'nested_level': parent_loops + 1,
            'type': 'for' if isinstance(loop_node, ast.For) else 'while'
        }
    
    def _analyze_function_call(self, call_node: ast.Call) -> List[str]:
        """Analyze function calls for complexity hints"""
        reasons = []
        
        if isinstance(call_node.func, ast.Name):
            func_name = call_node.func.id
            
            # Common O(n log n) functions
            if func_name in ['sorted', 'sort']:
                reasons.append('Sorting function detected (O(n log n))')
            
            # Common O(log n) functions
            elif func_name in ['bisect', 'binary_search']:
                reasons.append('Binary search detected (O(log n))')
            
            # Common O(n) functions
            elif func_name in ['sum', 'max', 'min', 'len']:
                reasons.append('Linear operation detected')
        
        return reasons
    
    def _compare_complexity(self, new_complexity: str, current_complexity: str) -> bool:
        """Compare two complexity notations and return True if new is worse"""
        complexity_order = [
            'O(1)', 'O(log n)', 'O(n)', 'O(n log n)', 
            'O(n²)', 'O(n³)', 'O(2^n)', 'O(n!)'
        ]
        
        try:
            new_idx = complexity_order.index(new_complexity)
            current_idx = complexity_order.index(current_complexity)
            return new_idx > current_idx
        except ValueError:
            # Handle custom complexities like O(n^4)
            if 'n^' in new_complexity and 'n^' not in current_complexity:
                return True
            return False
    
    def analyze_from_file(self, filepath: str) -> Dict:
        """Analyze code from a file"""
        try:
            with open(filepath, 'r') as file:
                code = file.read()
            return self.analyze_code(code)
        except FileNotFoundError:
            return {'error': f'File not found: {filepath}'}
        except Exception as e:
            return {'error': f'Error reading file: {str(e)}'}

def analyze_big_o(code_or_filepath: str, is_file: bool = False) -> None:
    """Convenience function to analyze and print results"""
    analyzer = BigOAnalyzer()
    
    if is_file:
        result = analyzer.analyze_from_file(code_or_filepath)
    else:
        result = analyzer.analyze_code(code_or_filepath)
    
    if 'error' in result:
        print(f"Error: {result['error']}")
        return
    
    print(f"Estimated Big O Complexity: {result['estimated_complexity']}")
    print(f"Confidence: {result['confidence']}")
    
    if result['reasons']:
        print("\nReasons:")
        for reason in result['reasons']:
            print(f"  • {reason}")
    
    if result['detailed_analysis']:
        print("\nDetailed Function Analysis:")
        for func_name, details in result['detailed_analysis'].items():
            print(f"  {func_name}(): {details['complexity']}")
            if details['reasons']:
                for reason in details['reasons']:
                    print(f"    - {reason}")

# Example usage and test cases
if __name__ == "__main__":
    # Test cases
    test_codes = [
        # O(1) - Constant time
        """
def constant_example(arr):
    return arr[0]
        """,
        
        # O(n) - Linear time
        """
def linear_search(arr, target):
    for i in range(len(arr)):
        if arr[i] == target:
            return i
    return -1
        """,
        
        # O(n²) - Quadratic time
        """
def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
        """,
        
        # O(2^n) - Exponential time
        """
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)
        """,
        
        # O(n log n) - Sort
        """
def merge_sort_wrapper(arr):
    return sorted(arr)
        """
    ]
    
    print("Big O Analyzer - Test Results")
    print("=" * 40)
    
    for i, code in enumerate(test_codes, 1):
        print(f"\nTest Case {i}:")
        print("-" * 20)
        analyze_big_o(code)
        print()