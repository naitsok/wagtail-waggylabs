from wagtail.snippets.views.snippets import SnippetViewSet


class PostCategoryViewSet(SnippetViewSet):
    """View set to add post categories to the admin menu."""
    icon = 'list-ul'
    menu_label = 'Categories'
    menu_name = 'post_categories'
    menu_order = 300
    add_to_admin_menu = True


class PostPageTagViewSet(SnippetViewSet):
    """View set to add post categories to the admin menu."""
    icon = 'tags'
    menu_label = 'Tags'
    menu_name = 'post_tags'
    menu_order = 300
    add_to_admin_menu = True
    
    
class PostPageViewSet(SnippetViewSet):
    """View set to add post pages shortcut to the admin menu."""
    icon = 'post-page'
    menu_label = 'Post pages'
    menu_name = 'post_pages'
    menu_order = 300
    add_to_admin_menu = True
    
    
class PostListPageViewSet(SnippetViewSet):
    """View set to add post list pages shortcut to the admin menu."""
    icon = 'post-list-page'
    menu_label = 'Post list pages'
    menu_name = 'post_list_pages'
    menu_order = 300
    add_to_admin_menu = True