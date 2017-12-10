# Algernon Algorithms Module
# By Nick Patrikeos from 7 March 2017 to 10 March 2017

# Random module required for randomisation
from random import randint, choice

class DivideConquer(object):
    # Class that implements methods that use divide and conquer to solve algorithmic problems
    
    def karatsuba_multiply(self, x, y):
        # Method to multiply 2 large numbers quickly
        
        if len(str(x)) == 1 or len(str(y)) == 1:
            # Base Case for small numbers
            return x * y
        else:
            
            # Find the middle length of the two numbers as strings
            n = max(len(str(x)), len(str(y)))
            m = n // 2

            
            # Calculate the four parts
            a = x // 10**(m)
            b = x % 10**(m)
            c = y // 10**(m)
            d = y % 10**(m)
            
            # Recursively compute the two subsequent products

            ac = self.karatsuba_multiply(a, c)
            bd = self.karatsuba_multiply(b, d)
            ad_bc = self.karatsuba_multiply(a+b, c+d) - ac - bd

            # Return the answer
            return ac * 10**(2*m) + (ad_bc * 10**m) + bd

    
    def inversion_count(self, lst):
        # Method to count the number of inversions in a list
        
        if len(lst) == 1:
            # Base case for list of length 1
            return (0, lst)
        
        m = (len(lst)-1) // 2
        x, lefthalf = self.inversion_count(lst[0:m+1])
        y, righthalf = self.inversion_count(lst[m+1:len(lst)])
        z, result = DivideConquer.merge_countsplitinv(lefthalf, righthalf, len(lst))

        return (x+y+z, result)

    @staticmethod
    def merge_countsplitinv(a, b, n):
        # Merges the input arrays and counts the number of inversions
        
        c = [ None for x in range(n) ]
        i = 0
        j = 0
        k = 0
        inversions = 0
        
        while i < len(a) and j < len(b):
            if a[i] < b[j]:
                c[k] = a[i]
                i += 1
            else:
                c[k] = b[j]
                j += 1
                inversions += 1
            k += 1
        
        # Find leftover elements
        while i < len(a):
            c[k] = a[i]
            i += 1
            k += 1
    
    
        while j < len(b):
            c[k] = b[j]
            j += 1
            k += 1
        
        return (inversions, c)
    

class Sorting(object):
    # Class that implements algorithms to sort an array

    def mergesort(self, lst):
        # Method to sort an array, uses divide and conquer
        
        if len(lst) == 1:
            # Return base case
            return lst
        
        # Find the middle and split the list
        m = (len(lst)-1) // 2
        
        # Recurse with both halves
        lefthalf = self.mergesort(lst[0:m+1])
        righthalf = self.mergesort(lst[m+1:len(lst)])
        
        # Merge the halves back together
        result = Sorting.merge(lefthalf, righthalf, len(lst))
        
        # Return the answer
        return result

    @staticmethod
    def merge(a,b,n):
        
        # Initialise variables
        c = [ None for x in range(n) ]
        i = 0
        j = 0
        k = 0

        # Go through a and b adding to c with k using i and j
        while i < len(a) and j < len(b):
            if a[i] < b[j]:
                c[k] = a[i]
                i += 1
            else:
                c[k] = b[j]
                j += 1
            k += 1

        # Any leftover elements in list a?
        while i < len(a):
            c[k] = a[i]
            i += 1
            k += 1

        # Any leftover elements in list b?
        while j < len(b):
            c[k] = b[j]
            j += 1
            k += 1
            
        # Return the merged product
        return c
    
    def d_quicksort(self, lst):
        # Method to sort an array by partitioning elements around a deterministically chosen pivot element
        ## Note that this method is IN PLACE
        
        # Calls helper
        Sorting.quicksort_helper(lst, 0, len(lst)-1)

    @staticmethod
    def quicksort_helper(lst, low, high):
        # This is a function which does the work, making calling of d_quicksort 
        # easier by not having to give more parameters than nessescary
        
        if low < high:
            # Partition around a pivot
            pivot_location = Sorting.partition(lst, low, high)
            
            # Recurse on the left and right parts of the list
            Sorting.quicksort_helper(lst, low, pivot_location-1)
            Sorting.quicksort_helper(lst, pivot_location + 1, high)

    @staticmethod
    def partition(lst, low, high):
        # Partitions an array around a pivot element in-place
        
        # Initialise variables
        pivot = lst[low]
        leftmark = low+1
        rightmark = high
        finished = False
        
        # Move the elements according to the pivot
        while not finished:
            while leftmark <= rightmark and lst[leftmark] <= pivot:
                leftmark += 1

            while lst[rightmark] >= pivot and rightmark >= leftmark:
                rightmark -= 1

            if rightmark < leftmark:
                finished = True
            else:
                t = lst[leftmark]
                lst[leftmark] = lst[rightmark]
                lst[rightmark] = t
        
        # Swap the pivot to its proper position
        t = lst[low]
        lst[low] = lst[rightmark]
        lst[rightmark] = t

        # Return the pivot index
        return rightmark

class Randomised(object):

    def r_quicksort(self, lst):
        # Method to sort an array by partitioning elements around a deterministically chosen pivot element
        # Note that this method is IN PLACE
        
        Randomised.rquicksort_helper(lst, 0, len(lst)-1)
    
    @staticmethod
    def rquicksort_helper(lst, low, high):
        # This is a function which does the work, making calling of r_quicksort 
        # easier by not having to give more parameters than nessescary
        
        if low < high:
            pivot_location = Randomised.partition(lst, low, high)
            Randomised.rquicksort_helper(lst, low, pivot_location-1)
            Randomised.rquicksort_helper(lst, pivot_location + 1, high)
    
    @staticmethod
    def partition(lst, start, end):
        # Partitions an array around a randomly chosen pivot element in place
        
        pivot = randint(start, end)
        
        # Set up initial pivot position
        temp = lst[end]
        lst[end] = lst[pivot]
        lst[pivot] = temp
        pivot_index = start

        # Partition the array around the pivot
        for i in range(start, end):
            if lst[i] <= lst[end]:
                temp = lst[i]
                lst[i] = lst[pivot_index]
                lst[pivot_index] = temp
                pivot_index += 1
                
        # Swap the pivot to its proper position
        temp1 = lst[end]
        lst[end] = lst[pivot_index]
        lst[pivot_index] = temp1

        # Return the pivot index
        return pivot_index
    
    def kmincut(self, graph):
        # Calls karger to find the minumim cut if a graph
        # Due to the potential failure of karger producing a mininum cut (A, B), multiple tests are run
        
        mincut = float('inf')
        
        for x in range(len(graph)):
            run_alg = Randomised.karger(graph)
            mincut = min(run_alg, mincut)
        
        return mincut
    
    @staticmethod
    def karger(graph):
        # Uses Karger's Contraction algorithm to find the minimum cut of a graph
        
        length = []
        
        # Until two supernodes remain, choose two random nodes and fuse them together
        while len(graph) > 2:
            vertex1, vertex2 = Randomised.chooseRandomKey(graph)
            graph[vertex1].extend(graph[vertex2])
            for x in graph[vertex2]:
                graph[x].remove(vertex2)
                graph[x].append(vertex1)
            while vertex1 in graph[vertex1]:
                graph[vertex1].remove(vertex1)
            del graph[vertex2]
        
        # Find the number of edges left
        for key in graph.keys():
            length.append(len(graph[key]))
        
        # Return the answer
        return length[0]
    
    @staticmethod
    def chooseRandomKey(graph):
        # Chooses a two random nodes to be contracted
        
        a = choice(list(graph.keys()))
        b = choice(list(graph[a]))
        return a, b

if __name__ == '__main__':
    x = DivideConquer()
    print(x.karatsuba_multiply(1234, 5678))
    y = Sorting()
    print(x.inversion_count([4, -1, 2, 7, 6, 8, 123])[0])
    print()
    print(y.mergesort([4, -1, 2, 7, 6, 8, 123]))
    yeeha = [4, -1, 2, 7, 6, 8, 123]
    y.d_quicksort(yeeha)
    print(yeeha)
    z = Randomised()
    yeeha = [4, -1, 2, 7, 6, 8, 123]
    z.r_quicksort(yeeha)
    print(yeeha)
    
    graph = {'A': ['B', 'C'],
         'B': ['A', 'D', 'E'],
         'C': ['A', 'F'],
         'D': ['B'],
         'E': ['B', 'F'],
         'F': ['C', 'E']}
    
    print(z.kmincut(graph))
