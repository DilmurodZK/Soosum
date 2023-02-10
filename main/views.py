from rest_framework.response import Response
from .serializer import *
from rest_framework.decorators import api_view


@api_view(['GET'])
def slider(request):
    slider = Slider.objects.last()
    ser = SliderSerializer(slider)
    return Response(ser.data)


@api_view(['POST'])
def client(request):
    name = request.POST.get("name")
    phone = request.POST.get("phone")
    Client.objects.create(
        name=name,
        phone=phone,
    )
    return Response('Success')


@api_view(['GET'])
def product(request):
    product = Product.objects.all()
    ser = ProductSerializer(product, many=True)
    return Response(ser.data)


@api_view(['GET'])
def about_product(request):
    about_product = About.objects.all()
    ser = AboutSerializer(about_product, many=True)
    return Response(ser.data)


@api_view(['GET'])
def advice(request):
    advice = Advice.objects.last()
    ser = AdviceSerializer(advice)
    return Response(ser.data)


@api_view(['GET'])
def advice_item(request):
    advice_item = AdviceItem.objects.all()
    ser = AdviceItemSerializer(advice_item, many=True)
    return Response(ser.data)

@api_view(['GET'])
def instruction(request):
    instruction = Instruction.objects.last()
    ser = InstructionSerializer(instruction)
    return Response(ser.data)


@api_view(['GET'])
def facts(request):
    facts = Facts.objects.all()
    ser = FactsSerializer(facts, many=True)
    return Response(ser.data)


@api_view(['GET'])
def factitem(request):
    fact_item = FactItem.objects.all()
    ser = FactItemSerializer(fact_item, many=True)
    return Response(ser.data)


@api_view(['GET'])
def info(request):
    info = Info.objects.last()
    ser = InfoSerializer(info)
    return Response(ser.data)

