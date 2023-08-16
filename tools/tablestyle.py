from reportlab.lib import colors

header_style                = [
                                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                                ('BOTTOMPADDING', (0, 0), (-1, -1), 20),
                                ('LINEBELOW', (0, 0), (-1, 0), 1, colors.grey),
                            ]

common_style                = [
                                ('BOX', (0, 0), (-1, -1), 0, colors.transparent),
                                ('GRID', (0, 0), (-1, -1), 0, colors.transparent),
                                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                                ('ALIGN', (0, 0), (-1, 0), 'RIGHT'),
                                ('FONTNAME', (0, 0), (-1, -1), 'NotoSansKR'),
                                ('FONTSIZE', (0, 0), (-1, -1), 5),
                                ('LEFTPADDING', (0, 0), (-1, -1), 1),
                                ('RIGHTPADDING', (0, 0), (-1, -1), 1),
                            ]

overview_style              = [
                                ('LINEABOVE', (0, 1), (-1, 1), 0.5, colors.grey),
                                ('ALIGN', (0, 0), (0, -1), 'LEFT'),
                                ('ALIGN', (1, 1), (-1, -1), 'RIGHT'),
                            ]

movers_style                = [
                                ('LINEABOVE', (0, 1), (-1, 1), 0.5, colors.grey),
                                ('ALIGN', (0, 0), (1, -1), 'LEFT'),
                                ('ALIGN', (2, 1), (-1, -1), 'RIGHT'),
                            ]

events_style                = [
                                ('LINEABOVE', (0, 3), (-1, 3), 0.5, colors.grey),
                                ('TOPPADDING', (0, 0), (-1, 1), 0),
                                ('BOTTOMPADDING', (0, 0), (-1, 1), 0),
                                ('ALIGN', (0, 0), (2, -1), 'LEFT'),
                                ('ALIGN', (3, 1), (-1, -1), 'RIGHT'),
                            ]

news_style                  = [
                                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                                ('TOPPADDING', (0, 0), (-1, -1), 0),
                                ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
                            ]