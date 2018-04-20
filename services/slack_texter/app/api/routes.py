from flask import Blueprint, jsonify, request, render_template, Response
import config
from twilio import twiml
from twilio.rest import Client
from twilio.twiml.messaging_response import Body, Message, Redirect, MessagingResponse
from slackclient import SlackClient
import json

tc = Client(config.twilio_sid, config.twilio_token)
sc = SlackClient(config.slack_token)



main_blueprint = Blueprint('main', __name__, template_folder='./templates')


@main_blueprint.route('/', methods=['GET'])
def index():
    return jsonify('Hello!')


@main_blueprint.route('/alive/ping', methods=['GET'])
def ping_pong():
    sc.api_call("chat.postMessage",
                as_user="False",
                channel="bot_testing_2",
                text="Hello!",
                username="Test")

    return jsonify({
        'message': 'pong!'
    })



@main_blueprint.route('/unnecessarily_long_obfuscated_url/incoming', methods=['POST'])
def incoming_texts():
    response = MessagingResponse()
    inbound_message = request.form


    json_payload = [
        {
            "color": "#36a64f",
            "text": " ",
            "fields": [
                {
                    "title": "From",
                    "value": inbound_message.get('From', None),
                    "short": True
                },
                {
                    "title": "Customer",
                    "value": " ",
                    "short": True
                },
                {
                    "title": "Message",
                    "value": inbound_message.get('Body', None),
                    "short": True
                }

            ],
            "actions": [
                {
                    "type": "button",
                    "text": "Link to Order",
                    "url": "https://"
                },
                {
                    "type": "button",
                    "text": "Link to Profile",
                    "url": "https://"
                }
            ]
        }
    ]

    sc.api_call("chat.postMessage",
                as_user="False",
                channel="bot_testing_2",
                text='`Customer Message`',
                attachments=json.dumps(json_payload),
                username="Customer Messaging")

    return Response(str(response), mimetype="application/xml"), 200


@main_blueprint.route('/unnecessarily_long_obfuscated_url/outgoing', methods=['GET','POST'])
def outgoing_texts():
    text = request.values.get('text')
    user = request.values.get('user_name')

    ph_start = text.find('ph:')
    message_start = text.find('text:')


    if ph_start >= 0 and message_start >= 0:
        phone_number = text[ph_start+4:ph_start+14]
        message_content = text[message_start+5:]

        try:
            tc.messages.create(to='+1'+phone_number,
                                from_=config.prod_number,
                                body=message_content)

            json_payload = [
                {
                    "color": "#36a64f",
                    "text": " ",
                    "fields": [
                        {
                            "title": "From",
                            "value": user,
                            "short": True
                        },
                        {
                            "title": "Customer",
                            "value": phone_number,
                            "short": True
                        },
                        {
                            "title": "Message",
                            "value": message_content,
                            "short": True
                        }

                    ],
                    "actions": [
                        {
                            "type": "button",
                            "text": "Link to Order",
                            "url": "https://"
                        },
                        {
                            "type": "button",
                            "text": "Link to Profile",
                            "url": "https://"
                        }
                    ]
                }
            ]
            sc.api_call("chat.postMessage",
                        as_user="False",
                        channel="bot_testing_2",
                        text='`Text sent to customer`',
                        attachments=json.dumps(json_payload),
                        username="Customer Messaging")

            return "Text delivered!", 200

        except:
            sc.api_call("chat.postMessage",
                        as_user="False",
                        channel="bot_testing_2",
                        text='Message Failed; Invalid format or phone number',
                        username="Customer Messaging")


            return "Message Exception!", 200

    return 'Message Failed', 200
