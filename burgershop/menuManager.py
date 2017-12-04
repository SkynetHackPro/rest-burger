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

        def node_iterator(nodes_ids):
            serialised = {}
            for pk in nodes_ids:
                node = nodes[pk]
                serialised[node.name] = {
                    'items': get_node_items(node),
                    'categories': node_iterator([i.pk for i in node.child.all()])
                }
            return serialised

        root_nodes = self.root_nodes().prefetch_related('child', 'items')
        nodes = {item.pk: item for item in self.all().prefetch_related('child', 'items')}
        return node_iterator([item.pk for item in root_nodes])
