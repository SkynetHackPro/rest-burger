from mptt.managers import TreeManager


class CategoryManager(TreeManager):
    def get_serialised_with_items(self):
        def get_node_items(node):
            serialised = {}
            for item in node.items.all():
                serialised[item.pk] = {
                    'name': item.name,
                    'price': str(item.price)
                }
            return serialised

        def node_iterator(nodes):
            serialised = {}
            for node in nodes:
                serialised[node.name] = {
                    'items': get_node_items(node),
                    'categories': node_iterator(node.child.all())
                }
            return serialised

        root_nodes = self.root_nodes().prefetch_related('child', 'items', 'child__items')
        return node_iterator(root_nodes)
