from django.shortcuts import render

def tes_review(request):
    # tes card review. will delete later. data all dummy
    filled_star_count = 4
    empty_star_count = 1

    stars = list(range(filled_star_count))
    empty_stars = list(range(empty_star_count))

    context = {
        'stars': stars,
        'empty_stars': empty_stars,
    }
    
    return render(request, "review_card.html", context)
