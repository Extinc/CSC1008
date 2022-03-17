class Node:
    def __init__(self,object):
        for i in object.items():
            self.object[i] = object[i]
            print(object[i]) 
        self.next = None

class SinglyLinkedList:
    def __init__(self):
        self.head = None
    #return the value of the node at index

    def search(self, index):
        temp = self.head
        prev = None
        counter = 0
        while temp is not None and counter < index:
            prev = temp
            temp = temp.next
            counter += 1

        if temp is None:
            print('search error: invalid index')
        else:
            return temp
    def insertAtEnd(self, object):
      NewNode = Node(object)
      if self.headval is None:
         self.headval = NewNode
         return
      laste = self.headval
      while(laste.nextval):
         laste = laste.nextval
      laste.nextval=NewNode

    def insertAtHead(self, node):
        if self.head is None:
            self.head = node
        else:
            node.next = self.head
            self.head = node

    def delete(self, value):
        prev = None
        temp = self.head

        while temp != None and temp.data != value:
            prev = temp
            temp = temp.next

        #node to be deleted is head
        if temp == self.head:
            self.deleteAtHead()

        #Value found
        elif temp != None:
            prev.next = temp.next
            del temp
        #Value not found
        else:
            print('Value ', value, ' cannot be found')

    #delete the node at index
    def deleteAt(self,index):
        temp = self.head
        prev = None
        counter = 0
        while temp is not None and counter < index:
            prev = temp
            temp = temp.next
            counter += 1

        if temp is None:
            print('search error: invalid index')
        else:
            if prev is None:
                self.head = temp.next
            else:
                prev.next = temp.next
            del temp

    def deleteAtHead(self):
        temp = self.head
        self.head = self.head.next
        del temp

    def printList(self):
        output = "Current list content: [ "
        temp = self.head
        while temp is not None:
            output += str(temp.data) + " "
            temp = temp.next
        output += "]"
        print(output)

    #return the number of elements in the queue
    def size(self):
        temp = self.head
        size = 0
        while temp is not None:
            size += 1
            temp = temp.next
        return size
