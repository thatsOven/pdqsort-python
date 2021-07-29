def swap(array, a, b):
    array[a], array[b] = array[b], array[a]

class MaxHeapSort:
    @staticmethod
    def siftDown(array, root, dist, a):
        while root <= dist // 2:
            leaf = 2 * root

            if leaf < dist and array[a + leaf - 1] < array[a + leaf]:
                leaf += 1

            if array[a + root - 1] < array[a + leaf - 1]:
                swap(array, a + root - 1, a + leaf - 1)
                root = leaf
            else: break

    @staticmethod
    def heapify(array, a, b):
        length = (b - a) // 1

        for i in range(length, 1, -1):
            MaxHeapSort.siftDown(array, i, length, a)

    @staticmethod
    def sort(array, a, b):
        MaxHeapSort.heapify(array, a, b)

        for i in range(b - a, 2, -1):
            swap(array, a, a + i - 1)
            MaxHeapSort.siftDown(array, 1, i - 1, a)

class PDQSort:
    insertSortThreshold    = 24
    nintherThreshold       = 128
    partialInsertSortLimit = 8
    blockSize              = 64
    cachelineSize          = 64

    @staticmethod
    def pdqLog(n):
        n >>= 1
        log = 0
        while n != 0:
            log += 1
            n >>= 1
        return n

    @staticmethod
    def insertSort(array, a, b):
        if a == b: return

        for i in range(a + 1, b):
            if array[i] < array[i - 1]:
                tmp = array[i]

                j = i - 1
                while array[j] > tmp and j >= a:
                    array[j + 1] = array[j]
                    j -= 1
                array[j + 1] = tmp

    @staticmethod
    def unguardInsertSort(array, a, b):
        if a == b: return

        for i in range(a + 1, b):
            if array[i] < array[i - 1]:
                tmp = array[i]

                j = i - 1
                while array[j] > tmp:
                    array[j + 1] = array[j]
                    j -= 1
                array[j + 1] = tmp

    @staticmethod
    def partialInsertSort(array, a, b):
        if a == b: return

        limit = 0
        for i in range(a + 1, b):
            if limit > PDQSort.partialInsertSortLimit: return False

            if array[i] < array[i - 1]:
                tmp = array[i]

                j = i - 1
                while array[j] > tmp and j >= a:
                    array[j + 1] = array[j]
                    j -= 1
                array[j + 1] = tmp

            limit += i - j + 1

        return True

    @staticmethod 
    def sortTwo(array, a, b):
        if array[b] < array[a]:
            swap(array, a, b)

    @staticmethod
    def sortThree(array, a, b, c):
        PDQSort.sortTwo(array, a, b)
        PDQSort.sortTwo(array, b, c)
        PDQSort.sortTwo(array, a, b)

    @staticmethod
    def partRight(array, a, b):
        pivot = array[a]

        first = a
        last  = b

        while True:
            first += 1
            if not (array[first] < pivot): break

        if first - 1 == a:
            while True:
                if not (first < last): break
                last -= 1
                if array[last] < pivot: break
        else:
            while True:
                last -= 1
                if array[last] < pivot: break

        alreadyParted = first >= last

        while first < last:
            swap(array, first, last)

            first += 1
            while array[first] < pivot:
                first += 1

            last -= 1
            while not (array[last] < pivot):
                last -= 1

        pivotPos = first - 1
        array[a] = array[pivotPos]
        array[pivotPos] = pivot

        return pivotPos, alreadyParted

    @staticmethod
    def partLeft(array, a, b):
        pivot = array[a]

        first = a
        last  = b

        while True:
            last -= 1
            if not (pivot < array[last]): break

        if last + 1 == b:
            while True:
                if not (first < last): break
                first += 1
                if pivot < array[first]: break
        else:
            while True:
                first += 1
                if pivot < array[first]: break

        while first < last:
            swap(array, first, last)

            last -= 1
            while pivot < array[last]:
                last -= 1

            first += 1
            while not (pivot < array[first]):
                first += 1

        pivotPos = last
        array[a] = array[pivotPos]
        array[pivotPos] = pivot

        return pivotPos

    @staticmethod
    def pdqLoop(array, a, b, badAllowed):
        leftmost = True

        while True:
            size = b - a

            if size < PDQSort.insertSortThreshold:
                if leftmost:
                    PDQSort.insertSort(array, a, b)
                else:
                    PDQSort.unguardInsertSort(array, a, b)
                return

            halfSize = size // 2

            if size > PDQSort.nintherThreshold:
                PDQSort.sortThree(array, a, a + halfSize, b - 1)
                PDQSort.sortThree(array, a + 1, a + (halfSize - 1), b - 2)
                PDQSort.sortThree(array, a + 2, a + (halfSize + 1), b - 3)
                PDQSort.sortThree(array, a + (halfSize - 1), a + halfSize, a + (halfSize + 1))
                swap(array, a, a + halfSize)
            else:
                PDQSort.sortThree(array, a, a + halfSize, b - 1)

            if (not leftmost) and (not array[a - 1] < array[a]):
                a = PDQSort.partLeft(array, a, b) + 1
                continue

            pivotPos, alreadyParted = PDQSort.partRight(array, a, b)

            leftSize  = pivotPos - a
            rightSize = b - (pivotPos + 1)

            highUnbalance = leftSize < size / 8 or rightSize < size / 8

            if highUnbalance:
                badAllowed -= 1
                if badAllowed == 0:
                    MaxHeapSort.sort(array, a, b)
                    return

                if leftSize >= PDQSort.insertSortThreshold:
                    swap(array, a, a + leftSize // 4)
                    swap(array, pivotPos - 1, pivotPos - leftSize // 4)

                    if leftSize > PDQSort.nintherThreshold:
                        swap(array, a + 1, a + (leftSize // 4 + 1))
                        swap(array, a + 2, a + (leftSize // 4 + 2))
                        swap(array, pivotPos - 2, pivotPos - (leftSize // 4 + 1))
                        swap(array, pivotPos - 3, pivotPos - (leftSize // 4 + 2))

                if rightSize >= PDQSort.insertSortThreshold:
                    swap(array, pivotPos + 1, pivotPos + (1 + rightSize // 4))
                    swap(array, b - 1, b - rightSize // 4)

                    if rightSize > PDQSort.nintherThreshold:
                        swap(array, pivotPos + 2, pivotPos + (2 + rightSize // 4))
                        swap(array, pivotPos + 3, pivotPos + (3 + rightSize // 4))
                        swap(array, b - 2, b - (1 + rightSize // 4))
                        swap(array, b - 3, b - (2 + rightSize // 4))
            elif (alreadyParted and PDQSort.partialInsertSort(array, a, pivotPos) 
                                and PDQSort.partialInsertSort(array, pivotPos + 1, b)):
                return

            PDQSort.pdqLoop(array, a, pivotPos, badAllowed)
            a = pivotPos + 1
            leftmost = False

def pdqSort(array, a, b):
    PDQSort.pdqLoop(array, a, b, PDQSort.pdqLog(b - a))