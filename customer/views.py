from django.shortcuts import render, get_object_or_404
from django.db.models import Avg, Count, Sum
from .models import Agent, Ticket, Rating, TicketStatus
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Article
from .forms import ArticleForm
from django.contrib.postgres.search import SearchVector
# from django.http import HttpResponse


# Create your views here.
@login_required
def key_metric_summary(request):
    # Get the ticket volume, average response time, resolution time, and customer satisfaction score.
    # ticket_volume = Ticket.objects.all().count()
    # average_response_time = Ticket.objects.all().aggregate(
    #     Avg('response_time'))['response_time__avg']
    # resolution_time = Ticket.objects.all().aggregate(
    #     Avg('resolution_time'))['resolution_time__avg']
    # customer_satisfaction_score = Ticket.objects.all().aggregate(
    #     Avg('customer_satisfaction_score'))['customer_satisfaction_score__avg']

    # # Get the last 3 lowest and highest 2 rated customer care representatives.
    # lowest_rated_representatives = Agent.objects.filter(
    #     ratings__score__lt=customer_satisfaction_score).order_by('-ratings__score')[:3]
    # highest_rated_representatives = Agent.objects.filter(
    #     ratings__score__gt=customer_satisfaction_score).order_by('ratings__score')[:2]

    # Render the template with the key metrics.
    context = {
        # 'ticket_volume': ticket_volume,
        # 'average_response_time': average_response_time,
        # 'resolution_time': resolution_time,
        # 'customer_satisfaction_score': customer_satisfaction_score,
        # 'lowest_rated_representatives': lowest_rated_representatives,
        # 'highest_rated_representatives': highest_rated_representatives,
    }
    return render(request, 'customer/key_metric_summary.html', context)

@login_required
def rating_records(request, agent_id):
    # Get the rating records for the specified agent.
    rating_records = Agent.objects.get(id=agent_id).ratings.all()

    # Render the template with the rating records.
    context = {
        'rating_records': rating_records,
    }
    return render(request, 'customer/rating_records.html', context)

@login_required
def line_or_area_charts(request):
    # Get the ticket volume and average response time for the past 30 days.
    # ticket_volume_data = Ticket.objects.all().order_by('-created_at').values('created_at').annotate(
    #     total_tickets=Count('id'))
    # response_time_data = Ticket.objects.all().order_by('-created_at').values('created_at').annotate(
    #     average_response_time=Avg('response_time'))

    # # Prepare data for line charts
    # line_chart_1_data = []
    # for data in ticket_volume_data:
    #     line_chart_1_data.append((data['created_at'], data['total_tickets']))

    # line_chart_2_data = []
    # for data in response_time_data:
    #     line_chart_2_data.append((data['created_at'], data['average_response_time']))

    # Render the template with the line chart data.
    context = {
        # 'line_chart_1_data': line_chart_1_data,
        # 'line_chart_2_data': line_chart_2_data,
    }
    return render(request, 'customer/line_or_area_charts.html', context)

@login_required
def gauges_or_kpi_cards(request):
    # Get the average resolution time and ticket volume for each agent.
    average_resolution_time_data = Agent.objects.all().annotate(
        average_resolution_time=Avg('tickets__resolution_time'))
    ticket_volume_data = Agent.objects.all().annotate(
        total_tickets=Count('tickets'))

    # Prepare data for gauges or KPI cards
    gauge_1_value = average_resolution_time_data.aggregate(Avg('average_resolution_time'))['average_resolution_time__avg']
    gauge_2_value = ticket_volume_data.aggregate(Sum('total_tickets'))['total_tickets__sum']

    # Render the template with the gauge values.
    context = {
        'gauge_1_value': gauge_1_value,
        'gauge_2_value': gauge_2_value,
    }
    return render(request, 'customer/gauges_or_kpi_cards.html', context)

@login_required
def performance_comparison(request):
    # Get the average resolution time and ticket volume for each agent.
    agents = Agent.objects.all()
    agent_data = []

    for agent in agents:
        average_resolution_time = agent.tickets.aggregate(Avg('resolution_time'))['resolution_time__avg']
        total_tickets = agent.tickets.count()
        agent_data.append((agent.name, average_resolution_time, total_tickets))

    # Render the template with the agent data.
    context = {
        'agent_data': agent_data,
    }
    return render(request, 'customer/performance_comparison.html', context)

@login_required
def response_time_analytics(request):
    # Calculate average response time for all tickets
    # average_response_time = Ticket.objects.all().aggregate(avg_response_time=Avg('response_time'))

    context = {
        # 'average_response_time': average_response_time['avg_response_time'],
    }
    return render(request, 'customer/response_time_analytics.html', context)

@login_required
def resolution_time_analytics(request):
    # Calculate average resolution time for all tickets
    # average_resolution_time = Ticket.objects.all().aggregate(avg_resolution_time=Avg('resolution_time'))

    context = {
        # 'average_resolution_time': average_resolution_time['avg_resolution_time'],
    }
    return render(request, 'customer/resolution_time_analytics.html', context)

@login_required
def customer_satisfaction_ratings(request):
    # Calculate average customer satisfaction ratings from the rating model
    average_customer_rating = Rating.objects.all().aggregate(avg_rating=Avg('score'))

    context = {
        'average_customer_rating': average_customer_rating['avg_rating'],
    }
    return render(request, 'customer/customer_satisfaction_ratings.html', context)

@login_required
def agent_performance_reports(request):
    # Calculate average resolution time and ticket volume for each agent
    agents = Agent.objects.all().annotate(
        avg_resolution_time=Avg('tickets__resolution_time'),
        total_tickets=Count('tickets')
    )

    context = {
        'agents': agents,
    }
    return render(request, 'customer/agent_performance_reports.html', context)

# Article creation and management

@login_required
def create_article(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            article = form.save(commit=False)
            article.author = request.user
            article.save()
            return redirect('article_detail', article_id=article.id)
    else:
        form = ArticleForm()
    
    context = {
        'form': form,
    }
    return render(request, 'customer/create_article.html', context)

@login_required
def edit_article(request, article_id):
    article = Article.objects.get(pk=article_id)
    if request.method == 'POST':
        form = ArticleForm(request.POST, instance=article)
        if form.is_valid():
            form.save()
            return redirect('article_detail', article_id=article.id)
    else:
        form = ArticleForm(instance=article)
    
    context = {
        'form': form,
        'article': article,
    }
    return render(request, 'customer/edit_article.html', context)

@login_required
def article_detail(request, article_id):
    article = Article.objects.get(pk=article_id)
    context = {
        'article': article,
    }
    return render(request, 'customer/article_detail.html', context)

@login_required
def search_articles(request):
    query = request.GET.get('q', '')
    articles = Article.objects.annotate(search=SearchVector('title', 'content')).filter(search=query)

    context = {
        'query': query,
        'articles': articles,
    }
    return render(request, 'customer/search_results.html', context)

@login_required
def update_ticket_status(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    # Implement logic to update the ticket status based on specific conditions
    # (e.g., based on time elapsed or customer request).
    # You can use forms to allow authorized users to update the status.

    return render(request, 'customer/ticket_status_update.html', {'ticket': ticket})

@login_required
def assign_ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    # Implement logic to assign the ticket to an agent.
    # You can use a dropdown form to select the agent for assignment.

    return render(request, 'customer/assign_ticket.html', {'ticket': ticket})

@login_required
def transfer_ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    # Implement logic to transfer the ticket from one agent to another.
    # You can use a dropdown form to select the new agent for the transfer.

    return render(request, 'customer/transfer_ticket.html', {'ticket': ticket})
