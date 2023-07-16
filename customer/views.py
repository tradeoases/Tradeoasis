from django.shortcuts import render
from django.db.models import Avg, Count, Sum
from .models import Agent, Ticket


# Create your views here.

def key_metric_summary(request):
    # Get the ticket volume, average response time, resolution time, and customer satisfaction score.
    ticket_volume = Ticket.objects.all().count()
    average_response_time = Ticket.objects.all().aggregate(
        Avg('response_time'))['response_time__avg']
    resolution_time = Ticket.objects.all().aggregate(
        Avg('resolution_time'))['resolution_time__avg']
    customer_satisfaction_score = Ticket.objects.all().aggregate(
        Avg('customer_satisfaction_score'))['customer_satisfaction_score__avg']

    # Get the last 3 lowest and highest 2 rated customer care representatives.
    lowest_rated_representatives = Agent.objects.filter(
        ratings__score__lt=customer_satisfaction_score).order_by('-ratings__score')[:3]
    highest_rated_representatives = Agent.objects.filter(
        ratings__score__gt=customer_satisfaction_score).order_by('ratings__score')[:2]

    # Render the template with the key metrics.
    context = {
        'ticket_volume': ticket_volume,
        'average_response_time': average_response_time,
        'resolution_time': resolution_time,
        'customer_satisfaction_score': customer_satisfaction_score,
        'lowest_rated_representatives': lowest_rated_representatives,
        'highest_rated_representatives': highest_rated_representatives,
    }
    return render(request, 'key_metric_summary.html', context)

def rating_records(request, agent_id):
    # Get the rating records for the specified agent.
    rating_records = Agent.objects.get(id=agent_id).ratings.all()

    # Render the template with the rating records.
    context = {
        'rating_records': rating_records,
    }
    return render(request, 'rating_records.html', context)

def line_or_area_charts(request):
    # Get the ticket volume and average response time for the past 30 days.
    ticket_volume_data = Ticket.objects.all().order_by('-created_at').values('created_at').annotate(
        total_tickets=Count('id'))
    response_time_data = Ticket.objects.all().order_by('-created_at').values('created_at').annotate(
        average_response_time=Avg('response_time'))

    # Prepare data for line charts
    line_chart_1_data = []
    for data in ticket_volume_data:
        line_chart_1_data.append((data['created_at'], data['total_tickets']))

    line_chart_2_data = []
    for data in response_time_data:
        line_chart_2_data.append((data['created_at'], data['average_response_time']))

    # Render the template with the line chart data.
    context = {
        'line_chart_1_data': line_chart_1_data,
        'line_chart_2_data': line_chart_2_data,
    }
    return render(request, 'line_or_area_charts.html', context)


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
    return render(request, 'gauges_or_kpi_cards.html', context)


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
    return render(request, 'performance_comparison.html', context)
